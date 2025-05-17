package com.example.fleetmisapplication.ui.manager

import android.os.Bundle
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.example.fleetmisapplication.ApiClient
import com.example.fleetmisapplication.R
import com.example.fleetmisapplication.utils.SessionManager
import kotlinx.coroutines.launch

class FleetManagerDashboardActivity : AppCompatActivity() {

    private lateinit var sessionManager: SessionManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_fleet_manager_dashboard)

        sessionManager = SessionManager(this)

        val txtSummary: TextView = findViewById(R.id.txtSummary)

        val token = sessionManager.fetchAuthToken()
        if (token != null) {
            lifecycleScope.launch {
                try {
                    val response = ApiClient.instance.getUserDashboard("Token $token")
                    if (response.isSuccessful) {
                        val data = response.body()
                        txtSummary.text = """
                            Vehicles: ${data?.totalVehicles}
                            Drivers: ${data?.totalDrivers}
                            Requestors: ${data?.totalRequestors}
                            Services: ${data?.totalServices}
                            Pending: ${data?.totalPendingRequests}
                            Completed: ${data?.totalCompletedRequests}
                            Alerts: ${data?.unreadAlertsCount}
                        """.trimIndent()
                    } else {
                        Toast.makeText(this@FleetManagerDashboardActivity, "Failed to load", Toast.LENGTH_SHORT).show()
                    }
                } catch (e: Exception) {
                    Toast.makeText(this@FleetManagerDashboardActivity, "Error: ${e.message}", Toast.LENGTH_LONG).show()
                }
            }
        }
    }
}