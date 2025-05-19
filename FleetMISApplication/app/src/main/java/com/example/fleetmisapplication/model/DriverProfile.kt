package com.example.fleetmisapplication.model

data class DriverProfile(
    val name: String,
    val email: String,
    val contact: String,
    val vehiclePlate: String?,
    val assignedVehicleId: Int?
)
