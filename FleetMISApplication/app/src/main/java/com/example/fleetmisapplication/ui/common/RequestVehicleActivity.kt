package com.example.fleetmisapplication.ui.common

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.fleetmisapplication.R
import com.example.fleetmisapplication.ApiClient
import com.example.fleetmisapplication.model.VehicleRequestBody
import com.example.fleetmisapplication.model.ApiResponse
import com.example.fleetmisapplication.utils.SessionManager
import android.content.Intent
import com.example.fleetmisapplication.ui.dashboard.FleetUsersDashboardActivity
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class RequestVehicleActivity : AppCompatActivity() {

    private lateinit var sessionManager: SessionManager
    private lateinit var locationInput: EditText
    private lateinit var destinationInput: EditText
    private lateinit var purposeInput: EditText
    private lateinit var requiredDateInput: EditText
    private lateinit var submitButton: Button
    private lateinit var cancelButton: Button // ✅ Add this

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_request_vehicle)

        sessionManager = SessionManager(this)

        // Bind views
        locationInput = findViewById(R.id.inputCurrentLocation)
        destinationInput = findViewById(R.id.inputDestination)
        purposeInput = findViewById(R.id.inputPurpose)
        requiredDateInput = findViewById(R.id.inputRequiredDate)
        submitButton = findViewById(R.id.btnSubmitRequest)
        cancelButton = findViewById(R.id.btnCancel) // ✅ Bind cancel button

        submitButton.setOnClickListener {
            submitVehicleRequest()
        }

        // ✅ Cancel button logic
        cancelButton.setOnClickListener {
            val intent = Intent(this, FleetUsersDashboardActivity::class.java)
            startActivity(intent)
            finish()
        }
    }

    private fun submitVehicleRequest() {
        val currentLocation = locationInput.text.toString().trim()
        val destination = destinationInput.text.toString().trim()
        val purpose = purposeInput.text.toString().trim()
        val requiredDate = requiredDateInput.text.toString().trim()
        val token = sessionManager.fetchAuthToken()

        if (token.isNullOrEmpty()) {
            Toast.makeText(this, "Authentication token missing", Toast.LENGTH_SHORT).show()
            return
        }

        if (currentLocation.isEmpty() || destination.isEmpty() || purpose.isEmpty() || requiredDate.isEmpty()) {
            Toast.makeText(this, "Please fill all fields", Toast.LENGTH_SHORT).show()
            return
        }

        val requestBody = VehicleRequestBody(
            currentLocation = currentLocation,
            destination = destination,
            purpose = purpose,
            requiredDate = requiredDate
        )

        Toast.makeText(this, "Submitting request...", Toast.LENGTH_SHORT).show()

        ApiClient.instance.submitRequest("Token $token", requestBody)
            .enqueue(object : Callback<ApiResponse> {
                override fun onResponse(call: Call<ApiResponse>, response: Response<ApiResponse>) {
                    if (response.isSuccessful) {
                        Toast.makeText(this@RequestVehicleActivity, "Trip request submitted!", Toast.LENGTH_LONG).show()
                        finish()
                    } else {
                        Toast.makeText(this@RequestVehicleActivity, "Submission failed: ${response.code()}", Toast.LENGTH_SHORT).show()
                    }
                }

                override fun onFailure(call: Call<ApiResponse>, t: Throwable) {
                    Toast.makeText(this@RequestVehicleActivity, "Error: ${t.localizedMessage}", Toast.LENGTH_LONG).show()
                }
            })
    }
}
