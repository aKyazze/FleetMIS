package com.example.fleetmisapplication.ui.driver

import android.os.Bundle
import android.util.Log
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.fleetmisapplication.ApiClient
import com.example.fleetmisapplication.R
import com.example.fleetmisapplication.model.DriverProfile
import com.example.fleetmisapplication.utils.SessionManager
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class DriverProfileActivity : AppCompatActivity() {

    private lateinit var txtName: TextView
    private lateinit var txtContact: TextView
    private lateinit var txtVehicle: TextView
    private lateinit var sessionManager: SessionManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_driver_profile)

        txtName = findViewById(R.id.txtName)
        txtContact = findViewById(R.id.txtContact)
        txtVehicle = findViewById(R.id.txtVehicle)

        sessionManager = SessionManager(this)

        txtName.text = "Loading driver profile..." // temporarily show this
        loadDriverProfile()
    }

    private fun loadDriverProfile() {
        val token = sessionManager.fetchAuthToken()
        if (token == null) {
            Toast.makeText(this, "Token not found", Toast.LENGTH_SHORT).show()
            return
        }

        ApiClient.instance.getDriverProfile("Token $token").enqueue(object : Callback<DriverProfile> {
            override fun onResponse(call: Call<DriverProfile>, response: Response<DriverProfile>) {
                if (response.isSuccessful) {
                    val profile = response.body()
                    if (profile != null) {
                        txtName.text = "Name: ${profile.name}"
                        txtContact.text = "Contact: ${profile.contact}"
                        txtVehicle.text = "Assigned Vehicle: ${profile.vehiclePlate ?: "None"}"
                    } else {
                        txtName.text = "No profile data"
                    }
                } else {
                    txtName.text = "Failed to load profile"
                    Log.e("DriverProfile", "Response failed: ${response.code()} - ${response.message()}")
                }
            }

            override fun onFailure(call: Call<DriverProfile>, t: Throwable) {
                txtName.text = "Error loading profile"
                Log.e("DriverProfile", "Network error", t)
                Toast.makeText(this@DriverProfileActivity, "Error: ${t.message}", Toast.LENGTH_LONG).show()
            }
        })
    }
}
