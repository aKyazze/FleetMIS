package com.example.fleetmisapplication.model

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.fleetmisapplication.R

class TripAdapter(
    private val tripList: List<Trip>,
    private val onActionClick: (Trip, String) -> Unit // Function passed for return action
) : RecyclerView.Adapter<TripAdapter.TripViewHolder>() {

    inner class TripViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val vehiclePlate: TextView = itemView.findViewById(R.id.vehiclePlate)
        val destination: TextView = itemView.findViewById(R.id.destination)
        val requestor: TextView = itemView.findViewById(R.id.requestor)
        val needDate: TextView = itemView.findViewById(R.id.needDate)
        val allocationTime: TextView = itemView.findViewById(R.id.allocationTime)
        val mileageAtAssignment: TextView = itemView.findViewById(R.id.mileageAtAssignment)
        //val returnButton: TextView = itemView.findViewById(R.id.completeBtn)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): TripViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_trip, parent, false)
        return TripViewHolder(view)
    }

    override fun onBindViewHolder(holder: TripViewHolder, position: Int) {
        val trip = tripList[position]

        holder.vehiclePlate.text = "Vehicle: ${trip.vehicle?.vehicle_plate ?: "N/A"}"
        holder.destination.text = "Destination: ${trip.destination}"
        holder.requestor.text = "Requested by: ${trip.requestor?.username ?: "Unknown"}"
        holder.needDate.text = "Need: ${trip.required_date ?: "--"}"
        holder.allocationTime.text = "Assigned: ${trip.time_of_allocation ?: "--"}"
        holder.mileageAtAssignment.text = "Current Mileage: ${trip.mileage_at_assignment ?: "--"}"

       // holder.returnButton.setOnClickListener {
       //     onActionClick(trip, "C")
       // }
    }

    override fun getItemCount(): Int = tripList.size
}
