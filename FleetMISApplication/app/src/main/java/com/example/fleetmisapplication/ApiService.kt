package com.example.fleetmisapplication

import com.example.fleetmisapplication.model.VehicleRequestBody
import com.example.fleetmisapplication.model.ApiResponse
import com.example.fleetmisapplication.model.DashboardResponse
import com.example.fleetmisapplication.model.UserRequest
import com.example.fleetmisapplication.LoginRequest
import com.example.fleetmisapplication.LoginResponse
import retrofit2.Call
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Headers
import retrofit2.http.POST

interface ApiService {

    // Login endpoint
    @Headers("Content-Type: application/json")
    @POST("api/login/")
    fun login(@Body request: LoginRequest): Call<LoginResponse>

    // Dashboard API for authenticated users
    @GET("api/fleet/dashboard/")
    suspend fun getUserDashboard(
        @Header("Authorization") token: String
    ): Response<DashboardResponse>

    // Submit Request API

    @POST("api/requests/create/")
    fun submitRequest(
        @Header("Authorization") token: String,
        @Body request: VehicleRequestBody
    ): Call<ApiResponse>

    // Track Requests API
    @GET("api/requests/user/")
    fun getUserRequests(
        @Header("Authorization") token: String
    ): Call<List<UserRequest>>


}
