package com.example.fleetmisapplication

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.example.fleetmisapplication.model.DashboardResponse
import com.example.fleetmisapplication.utils.SessionManager
import com.example.fleetmisapplication.ui.dashboard.FleetUsersDashboardActivity
import com.example.fleetmisapplication.ui.driver.FleetDriversDashboardActivity
import com.example.fleetmisapplication.ui.manager.FleetManagerDashboardActivity
import kotlinx.coroutines.launch
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class MainActivity : AppCompatActivity() {

    private lateinit var progressBar: ProgressBar
    private lateinit var usernameInput: EditText
    private lateinit var passwordInput: EditText
    private lateinit var loginButton: Button
    private lateinit var sessionManager: SessionManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        sessionManager = SessionManager(this)
        progressBar = findViewById(R.id.progressBar)
        usernameInput = findViewById(R.id.username_input)
        passwordInput = findViewById(R.id.password_input)
        loginButton = findViewById(R.id.login_button)

        loginButton.setOnClickListener {
            val username = usernameInput.text.toString().trim()
            val password = passwordInput.text.toString().trim()

            if (username.isEmpty() || password.isEmpty()) {
                Toast.makeText(this, "Please fill in all fields", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            progressBar.visibility = View.VISIBLE

            val request = LoginRequest(username, password)
            ApiClient.instance.login(request).enqueue(object : Callback<LoginResponse> {
                override fun onResponse(call: Call<LoginResponse>, response: Response<LoginResponse>) {
                    progressBar.visibility = View.GONE
                    if (response.isSuccessful) {
                        val loginResponse = response.body()
                        if (loginResponse != null) {
                            sessionManager.saveAuthToken(
                                loginResponse.token,
                                loginResponse.username,
                                loginResponse.user_id
                            )

                            Toast.makeText(this@MainActivity, "Welcome ${loginResponse.username}", Toast.LENGTH_SHORT).show()

                            // Load dashboard and redirect based on role
                            loadAndRedirectDashboard("Token ${loginResponse.token}")
                        }
                    } else {
                        Toast.makeText(this@MainActivity, "Invalid credentials", Toast.LENGTH_SHORT).show()
                    }
                }

                override fun onFailure(call: Call<LoginResponse>, t: Throwable) {
                    progressBar.visibility = View.GONE
                    Toast.makeText(this@MainActivity, "Login failed: ${t.message}", Toast.LENGTH_LONG).show()
                }
            })
        }
    }

    private fun loadAndRedirectDashboard(token: String) {
        lifecycleScope.launch {
            try {
                val response = ApiClient.instance.getUserDashboard(token)
                if (response.isSuccessful) {
                    val dashboardData = response.body()
                    when (dashboardData?.role) {
                        "FleetUser" -> {
                            startActivity(Intent(this@MainActivity, FleetUsersDashboardActivity::class.java))
                        }
                        "FleetDriver" -> {
                            startActivity(Intent(this@MainActivity, FleetDriversDashboardActivity::class.java))
                        }
                        "FleetManager" -> {
                            startActivity(Intent(this@MainActivity, FleetManagerDashboardActivity::class.java))
                        }
                        else -> {
                            Toast.makeText(this@MainActivity, "Access denied. No role assigned.", Toast.LENGTH_LONG).show()
                        }
                    }
                    finish()
                } else {
                    Toast.makeText(this@MainActivity, "Failed to load dashboard data", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(this@MainActivity, "Error: ${e.message}", Toast.LENGTH_LONG).show()
            }
        }
    }
}
