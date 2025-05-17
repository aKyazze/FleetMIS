package com.example.fleetmisapplication

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class TripRecordsActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // You can create a custom layout later
        setContentView(android.R.layout.simple_list_item_1)
        title = "Trip Records"
    }
}
