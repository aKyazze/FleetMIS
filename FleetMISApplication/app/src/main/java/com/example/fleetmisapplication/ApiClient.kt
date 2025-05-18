

// ApiClient.kt
package com.example.fleetmisapplication

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object ApiClient {

    // use localhost for Android Emulator
   // private const val BASE_URL = "http://10.0.2.2:8000/"

    // use real Android Device for demonstration
   // private const val BASE_URL = "http://192.168.7.92:8000/"

    private const val BASE_URL = "http://127.0.0.1:8000/"




    val instance: ApiService by lazy {
        val retrofit = Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        retrofit.create(ApiService::class.java)
    }
}
