package com.example.fleetmisapplication

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object ApiClient {

    // For Android Emulator to connect to your PC localhost
     private const val BASE_URL = "http://10.0.2.2:8000/"

    // If you're using a real Android device, set your PC's local IP address:
    // private const val BASE_URL = "http://192.168.1.100:8000/"
    //private const val BASE_URL = "http://127.0.0.1:8000/"


    val instance: ApiService by lazy {
        val retrofit = Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        retrofit.create(ApiService::class.java)
    }
}
