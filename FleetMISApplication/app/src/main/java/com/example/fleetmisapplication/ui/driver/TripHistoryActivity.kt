package com.example.fleetmisapplication.ui.driver

import android.os.Bundle
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.fleetmisapplication.ApiClient
import com.example.fleetmisapplication.R
import com.example.fleetmisapplication.model.Trip
import com.example.fleetmisapplication.model.TripHistoryAdapter
import com.example.fleetmisapplication.utils.SessionManager
import kotlinx.coroutines.launch

class TripHistoryActivity : AppCompatActivity() {

    private lateinit var tripsRecyclerView: RecyclerView
    private lateinit var tripAdapter: TripHistoryAdapter
    private lateinit var titleText: TextView
    private lateinit var sessionManager: SessionManager
    private val tripList = mutableListOf<Trip>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_trip_history)

        tripsRecyclerView = findViewById(R.id.tripsRecyclerView)
        titleText = findViewById(R.id.titleText)
        sessionManager = SessionManager(this)

        tripsRecyclerView.layoutManager = LinearLayoutManager(this)
        tripAdapter = TripHistoryAdapter(tripList)
        tripsRecyclerView.adapter = tripAdapter

        fetchCompletedTrips()
    }

    private fun fetchCompletedTrips() {
        val token = sessionManager.fetchAuthToken() ?: return

        lifecycleScope.launch {
            try {
                val response = ApiClient.instance.getAssignedTrips("Token $token")  // or getTripHistory() if available
                if (response.isSuccessful) {
                    val allTrips = response.body() ?: emptyList()
                    val completedTrips = allTrips.filter { it.request_status == "C" }

                    tripList.clear()
                    tripList.addAll(completedTrips)
                    tripAdapter.notifyDataSetChanged()

                    // Update title
                    titleText.text = "Trips Completed: ${completedTrips.size}"
                } else {
                    Toast.makeText(this@TripHistoryActivity, "Failed to load trips", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(this@TripHistoryActivity, "Error: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
            }
        }
    }
}
