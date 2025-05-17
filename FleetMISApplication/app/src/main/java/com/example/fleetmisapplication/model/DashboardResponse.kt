package com.example.fleetmisapplication.model

data class DashboardResponse(
    val name: String,
    val role: String,
    val pendingRequests: Int? = null,
    val approvedRequests: Int? = null,
    val completedRequests: Int? = null,
    val totalVehicles: Int? = null,
    val totalDrivers: Int? = null,
    val totalRequestors: Int? = null,
    val totalServices: Int? = null,
    val totalServiceProviders: Int? = null,
    val totalPendingRequests: Int? = null,
    val totalCompletedRequests: Int? = null,
    val unreadAlertsCount: Int? = null
)