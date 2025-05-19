package com.example.fleetmisapplication.model

data class Trip(
    val id: Int,
    val vehicle: Vehicle,
    val destination: String,
    val requestor: Requestor,
    val required_date: String,
    val time_of_allocation: String,
    val request_status: String,
    val mileage_at_assignment: Int?,
    val mileage_at_return: Int?
)

data class Vehicle(
    val id: Int,
    val vehicle_plate: String
)

data class Requestor(
    val id: Int,
    val username: String
)
