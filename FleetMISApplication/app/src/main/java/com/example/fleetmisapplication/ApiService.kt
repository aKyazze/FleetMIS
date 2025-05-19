package com.example.fleetmisapplication

import com.example.fleetmisapplication.model.*
import retrofit2.Call
import retrofit2.Response
import retrofit2.http.*

interface ApiService {

    @Headers("Content-Type: application/json")
    @POST("api/login/")
    fun login(@Body request: LoginRequest): Call<LoginResponse>

    @GET("api/fleet/dashboard/")
    suspend fun getUserDashboard(
        @Header("Authorization") token: String
    ): Response<DashboardResponse>

    @POST("api/requests/create/")
    fun submitRequest(
        @Header("Authorization") token: String,
        @Body request: VehicleRequestBody
    ): Call<ApiResponse>

    @GET("api/requests/user/")
    fun getUserRequests(
        @Header("Authorization") token: String
    ): Call<List<UserRequest>>

    @GET("api/driver/profile/")
    fun getDriverProfile(
        @Header("Authorization") token: String
    ): Call<DriverProfile>

    @GET("api/driver/assigned_trips/")
    fun getDriverAssignedTrips(
        @Header("Authorization") token: String
    ): Call<List<TripData>>

    @GET("api/driver/trip_history/")
    fun getTripHistory(
        @Header("Authorization") token: String
    ): Call<List<TripData>>

    @GET("api/trips/assigned/")
    suspend fun getAssignedTrips(
        @Header("Authorization") token: String
    ): Response<List<Trip>>

    @POST("api/trips/return/{vehicleId}/")
    suspend fun returnVehicle(
        @Header("Authorization") token: String,
        @Path("vehicleId") vehicleId: Int
    ): Response<Void>

    // ✅ New: Update trip status and mileage (Start or Complete trip)
    @POST("api/driver/update_trip/{requestId}/")
    suspend fun updateTripStatus(
        @Header("Authorization") token: String,
        @Path("requestId") requestId: Int,
        @Body updateRequest: TripUpdateRequestBody
    ): Response<ApiResponse>
}
