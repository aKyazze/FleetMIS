package com.example.fleetmisapplication.ui.driver

import android.os.Bundle
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.fleetmisapplication.R

class DriverProfileActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_driver_profile)

        val txtName: TextView = findViewById(R.id.txtDriverName)
        val txtContact: TextView = findViewById(R.id.txtDriverContact)
        val txtEmail: TextView = findViewById(R.id.txtDriverEmail)
        val txtAssignedVehicle: TextView = findViewById(R.id.txtAssignedVehicle)

        // TODO: Replace with real API data from /api/driver/profile/
        Toast.makeText(this, "Loading driver profile...", Toast.LENGTH_SHORT).show()

        txtName.text = "Abdul-Rasheed Kyazze"
        txtContact.text = "+256 700 000 000"
        txtEmail.text = "abdul@example.com"
        txtAssignedVehicle.text = "UBD 123A (Toyota Land Cruiser)"
    }
}
