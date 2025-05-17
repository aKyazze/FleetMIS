package com.example.fleetmisapplication.ui.driver

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.example.fleetmisapplication.ApiClient
import com.example.fleetmisapplication.MainActivity
import com.example.fleetmisapplication.databinding.ActivityFleetDriverDashboardBinding
import com.example.fleetmisapplication.ui.common.RequestVehicleActivity
import com.example.fleetmisapplication.utils.SessionManager
import kotlinx.coroutines.launch

class FleetDriversDashboardActivity : AppCompatActivity() {

    private lateinit var binding: ActivityFleetDriverDashboardBinding
    private lateinit var sessionManager: SessionManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityFleetDriverDashboardBinding.inflate(layoutInflater)
        setContentView(binding.root)

        sessionManager = SessionManager(this)

        loadDashboard()

        binding.btnAssignedTrips.setOnClickListener {
            startActivity(Intent(this, AssignedTripsActivity::class.java))
        }

        binding.btnTripHistory.setOnClickListener {
            startActivity(Intent(this, TripHistoryActivity::class.java))
        }

        binding.btnDriverProfile.setOnClickListener {
            startActivity(Intent(this, DriverProfileActivity::class.java))
        }

        binding.btnRequestVehicle.setOnClickListener {
            startActivity(Intent(this, RequestVehicleActivity::class.java))
        }

        binding.btnLogout.setOnClickListener {
            sessionManager.clearToken()
            startActivity(Intent(this, MainActivity::class.java))
            finish()
        }
    }

    private fun loadDashboard() {
        val token = sessionManager.fetchAuthToken() ?: return

        lifecycleScope.launch {
            try {
                val response = ApiClient.instance.getUserDashboard("Token $token")
                if (response.isSuccessful) {
                    val dashboardData = response.body()
                    binding.txtWelcome.text = "Welcome, ${dashboardData?.name}"
                    binding.txtTrips.text = "Trips Completed: ${dashboardData?.completedRequests ?: 0}"
                } else {
                    Toast.makeText(this@FleetDriversDashboardActivity, "Failed to load dashboard", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(this@FleetDriversDashboardActivity, "Error: ${e.message}", Toast.LENGTH_LONG).show()
            }
        }
    }
}