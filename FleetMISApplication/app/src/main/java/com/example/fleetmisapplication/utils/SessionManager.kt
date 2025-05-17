package com.example.fleetmisapplication.utils

import android.content.Context
import android.content.SharedPreferences

class SessionManager(context: Context) {

    private var prefs: SharedPreferences = context.getSharedPreferences("FleetMIS", Context.MODE_PRIVATE)

    companion object {
        const val USER_TOKEN = "token"
        const val USERNAME = "username"
        const val USER_ID = "user_id"
    }

    fun saveAuthToken(token: String, username: String, userId: Int) {
        val editor = prefs.edit()
        editor.putString(USER_TOKEN, token)
        editor.putString(USERNAME, username)
        editor.putInt(USER_ID, userId)
        editor.apply()
    }

    fun fetchAuthToken(): String? {
        return prefs.getString(USER_TOKEN, null)
    }

    fun fetchUsername(): String? {
        return prefs.getString(USERNAME, null)
    }

    fun fetchUserId(): Int {
        return prefs.getInt(USER_ID, -1)
    }

    fun clearToken() {
        prefs.edit().clear().apply()
    }
}
