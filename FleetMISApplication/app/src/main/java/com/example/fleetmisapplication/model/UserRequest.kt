package com.example.fleetmisapplication.model

import com.google.gson.annotations.SerializedName

data class UserRequest(
    val id: Int,

    @SerializedName("current_location")
    val currentLocation: String,

    val destination: String,
    val purpose: String,

    @SerializedName("request_date")
    val requestDate: String,

    @SerializedName("required_date")
    val requiredDate: String,

    @SerializedName("request_status")
    val requestStatus: String,

    val vehicle: VehicleDetails?,  // Nullable — handled safely
    val driver: DriverDetails?     // Nullable — handled safely
)

data class VehicleDetails(
    val id: Int,

    @SerializedName("vehicle_plate")
    val vehiclePlate: String
)

data class DriverDetails(
    val id: Int,

    @SerializedName("driver_name")
    val driverName: String,

    val contact: String
)
