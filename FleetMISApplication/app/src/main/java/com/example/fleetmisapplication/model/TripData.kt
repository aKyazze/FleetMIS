// TripData.kt
package com.example.fleetmisapplication.model

data class TripData(
    val tripId: Int,
    val vehicleId: Int,
    val startTime: String, // ISO 8601 string or Date depending on your backend
    val endTime: String?,
    val origin: String,
    val destination: String,
    val status: String
)
