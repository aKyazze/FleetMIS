
package com.example.fleetmisapplication.model

data class TripUpdateRequestBody(
    val mileageAtAssignment: Int? = null,
    val mileageAtReturn: Int? = null,
    val requestStatus: String
)
