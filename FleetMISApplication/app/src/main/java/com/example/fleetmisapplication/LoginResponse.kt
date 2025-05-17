package com.example.fleetmisapplication

data class LoginResponse(
    val token: String,
    val user_id: Int,
    val username: String,
    val email: String,
    val role: String
)
