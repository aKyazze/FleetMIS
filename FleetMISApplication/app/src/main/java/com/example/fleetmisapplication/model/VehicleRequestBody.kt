package com.example.fleetmisapplication.model

data class VehicleRequestBody(
    val currentLocation: String,
    val destination: String,
    val purpose: String,
    val requiredDate: String
)
