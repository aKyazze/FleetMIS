package com.example.fleetmisapplication.ui.common

import android.app.DatePickerDialog
import android.content.Intent
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.example.fleetmisapplication.R
import com.example.fleetmisapplication.ApiClient
import com.example.fleetmisapplication.model.VehicleRequestBody
import com.example.fleetmisapplication.model.ApiResponse
import com.example.fleetmisapplication.utils.SessionManager
import com.example.fleetmisapplication.ui.dashboard.FleetUsersDashboardActivity
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.text.SimpleDateFormat
import java.util.*

class RequestVehicleActivity : AppCompatActivity() {

    private lateinit var sessionManager: SessionManager
    private lateinit var locationInput: EditText
    private lateinit var destinationInput: EditText
    private lateinit var purposeInput: EditText
    private lateinit var requiredDateInput: EditText
    private lateinit var submitButton: Button
    private lateinit var cancelButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_request_vehicle)

        sessionManager = SessionManager(this)

        locationInput = findViewById(R.id.inputCurrentLocation)
        destinationInput = findViewById(R.id.inputDestination)
        purposeInput = findViewById(R.id.inputPurpose)
        requiredDateInput = findViewById(R.id.inputRequiredDate)
        submitButton = findViewById(R.id.btnSubmitRequest)
        cancelButton = findViewById(R.id.btnCancel)

        // ✅ Show DatePickerDialog on clicking requiredDateInput
        requiredDateInput.setOnClickListener {
            showDatePickerDialog()
        }

        submitButton.setOnClickListener {
            submitVehicleRequest()
        }

        cancelButton.setOnClickListener {
            startActivity(Intent(this, FleetUsersDashboardActivity::class.java))
            finish()
        }
    }

    private fun showDatePickerDialog() {
        val calendar = Calendar.getInstance()
        val datePicker = DatePickerDialog(
            this,
            { _, year, month, day ->
                val pickedDate = Calendar.getInstance()
                pickedDate.set(year, month, day)
                val sdf = SimpleDateFormat("yyyy-MM-dd", Locale.US)
                requiredDateInput.setText(sdf.format(pickedDate.time))
            },
            calendar.get(Calendar.YEAR),
            calendar.get(Calendar.MONTH),
            calendar.get(Calendar.DAY_OF_MONTH)
        )
        // ✅ Prevent past dates
        datePicker.datePicker.minDate = calendar.timeInMillis
        datePicker.show()
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
            currentLocation, destination, purpose, requiredDate
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
