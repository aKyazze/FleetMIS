package com.example.fleetmisapplication.ui.driver

import android.app.AlertDialog
import android.os.Bundle
import android.view.LayoutInflater
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.fleetmisapplication.ApiClient
import com.example.fleetmisapplication.R
import com.example.fleetmisapplication.model.Trip
import com.example.fleetmisapplication.model.TripAdapter
import com.example.fleetmisapplication.model.TripUpdateRequestBody
import com.example.fleetmisapplication.utils.SessionManager
import kotlinx.coroutines.launch

class AssignedTripsActivity : AppCompatActivity() {

    private lateinit var recyclerView: RecyclerView
    private lateinit var adapter: TripAdapter
    private lateinit var sessionManager: SessionManager
    private val trips = mutableListOf<Trip>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_assigned_trips)

        recyclerView = findViewById(R.id.tripsRecyclerView)
        sessionManager = SessionManager(this)

        adapter = TripAdapter(trips) { trip, action ->
            showMileageDialog(trip, action)
        }

        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = adapter

        fetchAssignedTrips()
    }

    private fun fetchAssignedTrips() {
        val token = sessionManager.fetchAuthToken() ?: return
        lifecycleScope.launch {
            try {
                val response = ApiClient.instance.getAssignedTrips("Token $token")
                if (response.isSuccessful) {
                    trips.clear()
                    trips.addAll(response.body() ?: emptyList())
                    adapter.notifyDataSetChanged()
                } else {
                    Toast.makeText(this@AssignedTripsActivity, "Failed to load trips", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(this@AssignedTripsActivity, "Error: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun showMileageDialog(trip: Trip, action: String) {
        val token = sessionManager.fetchAuthToken() ?: return
        val builder = AlertDialog.Builder(this)
        val inflater = LayoutInflater.from(this)
        val view = inflater.inflate(R.layout.dialog_mileage_input, null)
        val mileageInput = view.findViewById<EditText>(R.id.editMileage)

        builder.setView(view)
            .setTitle(if (action == "O") "Start Trip" else "Complete Trip")
            .setPositiveButton("Submit") { _, _ ->
                val mileage = mileageInput.text.toString().toIntOrNull()
                if (mileage == null) {
                    Toast.makeText(this, "Enter valid mileage", Toast.LENGTH_SHORT).show()
                    return@setPositiveButton
                }

                val update = TripUpdateRequestBody(
                    mileageAtAssignment = if (action == "O") mileage else null,
                    mileageAtReturn = if (action == "C") mileage else null,
                    requestStatus = action
                )

                lifecycleScope.launch {
                    try {
                        val response = ApiClient.instance.updateTripStatus("Token $token", trip.id, update)
                        if (response.isSuccessful) {
                            Toast.makeText(this@AssignedTripsActivity, "Trip updated", Toast.LENGTH_SHORT).show()
                            fetchAssignedTrips()
                        } else {
                            Toast.makeText(this@AssignedTripsActivity, "Failed to update trip", Toast.LENGTH_SHORT).show()
                        }
                    } catch (e: Exception) {
                        Toast.makeText(this@AssignedTripsActivity, "Error: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
                    }
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }
}
