package com.example.fleetmisapplication.ui.driver

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.fleetmisapplication.R

class TripHistoryActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_trip_history)
        // TODO: Show completed trip history for driver
        Toast.makeText(this, "Fetching trip history...", Toast.LENGTH_SHORT).show()
    }
}