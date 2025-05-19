package com.example.fleetmisapplication.ui.dashboard

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.example.fleetmisapplication.ApiClient
import com.example.fleetmisapplication.MainActivity
import com.example.fleetmisapplication.databinding.ActivityFleetUserDashboardBinding
import com.example.fleetmisapplication.ui.common.RequestVehicleActivity
import com.example.fleetmisapplication.ui.common.TrackMyRequestsActivity
import com.example.fleetmisapplication.utils.SessionManager
import kotlinx.coroutines.launch

class FleetUsersDashboardActivity : AppCompatActivity() {

    private lateinit var binding: ActivityFleetUserDashboardBinding
    private lateinit var sessionManager: SessionManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityFleetUserDashboardBinding.inflate(layoutInflater)
        setContentView(binding.root)

        sessionManager = SessionManager(this)

        loadDashboard()

        // 🚗 Request Vehicle
        binding.btnRequestVehicle.setOnClickListener {
            startActivity(Intent(this, RequestVehicleActivity::class.java))
        }

        // 📋 Track My Requests
        binding.btnTrackRequests.setOnClickListener {
            startActivity(Intent(this, TrackMyRequestsActivity::class.java))
        }

        // 📤 Logout
        binding.btnLogout.setOnClickListener {
            sessionManager.clearToken()
            val intent = Intent(this, MainActivity::class.java)
            startActivity(intent)
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
                    binding.txtPendingRequests.text = "Pending Requests: ${dashboardData?.pendingRequests ?: 0}"
                    binding.txtApprovedRequests.text = "Approved Requests: ${dashboardData?.approvedRequests ?: 0}"  // <-- Add this line
                    binding.txtTrips.text = "Completed Trips: ${dashboardData?.completedRequests ?: 0}"
                } else {
                    Toast.makeText(this@FleetUsersDashboardActivity, "Failed to load dashboard", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(this@FleetUsersDashboardActivity, "Error: ${e.message}", Toast.LENGTH_LONG).show()
            }
        }
    }
}
