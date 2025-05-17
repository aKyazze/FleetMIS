package com.example.fleetmisapplication.ui.driver

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.fleetmisapplication.R

class AssignedTripsActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_assigned_trips)
        // TODO: Fetch driver assigned trips from /api/requests/driver/
        Toast.makeText(this, "Loading assigned trips...", Toast.LENGTH_SHORT).show()
    }
}