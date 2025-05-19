package com.example.fleetmisapplication.ui.common

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.fleetmisapplication.ApiClient
import com.example.fleetmisapplication.R
import com.example.fleetmisapplication.model.UserRequest
import com.example.fleetmisapplication.ui.dashboard.FleetUsersDashboardActivity
import com.example.fleetmisapplication.utils.SessionManager
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class TrackMyRequestsActivity : AppCompatActivity() {

    private lateinit var recyclerView: RecyclerView
    private lateinit var sessionManager: SessionManager
    private lateinit var adapter: RequestsAdapter
    private lateinit var backButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_track_my_requests)

        sessionManager = SessionManager(this)
        recyclerView = findViewById(R.id.recyclerRequests)
        backButton = findViewById(R.id.btnBack)

        adapter = RequestsAdapter()
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = adapter

        backButton.setOnClickListener {
            val intent = Intent(this, FleetUsersDashboardActivity::class.java)
            startActivity(intent)
            finish()
        }

        fetchUserRequests()
    }

    private fun fetchUserRequests() {
        val token = sessionManager.fetchAuthToken() ?: return

        ApiClient.instance.getUserRequests("Token $token")
            .enqueue(object : Callback<List<UserRequest>> {
                override fun onResponse(call: Call<List<UserRequest>>, response: Response<List<UserRequest>>) {
                    if (response.isSuccessful) {
                        val requests = response.body() ?: emptyList()
                        adapter.submitList(requests)
                    } else {
                        Toast.makeText(this@TrackMyRequestsActivity, "Failed to fetch requests", Toast.LENGTH_SHORT).show()
                    }
                }

                override fun onFailure(call: Call<List<UserRequest>>, t: Throwable) {
                    Toast.makeText(this@TrackMyRequestsActivity, "Error: ${t.message}", Toast.LENGTH_SHORT).show()
                }
            })
    }
}
