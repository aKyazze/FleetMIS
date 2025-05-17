package com.example.fleetmisapplication.ui.common

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.fleetmisapplication.R
import com.example.fleetmisapplication.model.UserRequest

class RequestsAdapter : RecyclerView.Adapter<RequestsAdapter.RequestViewHolder>() {

    private var requests = listOf<UserRequest>()

    fun submitList(data: List<UserRequest>) {
        requests = data
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RequestViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_request, parent, false)
        return RequestViewHolder(view)
    }

    override fun onBindViewHolder(holder: RequestViewHolder, position: Int) {
        holder.bind(requests[position])
    }

    override fun getItemCount(): Int = requests.size

    class RequestViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val txtDestination: TextView = itemView.findViewById(R.id.txtDestination)
        private val txtStatus: TextView = itemView.findViewById(R.id.txtStatus)
        private val txtVehicle: TextView = itemView.findViewById(R.id.txtVehicle)
        private val txtDriver: TextView = itemView.findViewById(R.id.txtDriver)
        private val txtDriverContact: TextView = itemView.findViewById(R.id.txtDriverContact)
        private val txtDates: TextView = itemView.findViewById(R.id.txtDates)

        fun bind(request: UserRequest) {
            txtDestination.text = "To: ${request.destination}"
            txtStatus.text = "Status: ${statusText(request.requestStatus)}"
            txtVehicle.text = "Vehicle: ${request.vehicle?.vehiclePlate ?: "Not Assigned"}"
            txtDriver.text = "Driver: ${request.driver?.driverName ?: "N/A"}"
            txtDriverContact.text = "Driver Contact: ${request.driver?.contact ?: "N/A"}"
            txtDates.text = "Dates: ${request.requestDate ?: "N/A"} → ${request.requiredDate ?: "N/A"}"
        }

        private fun statusText(code: String): String {
            return when (code) {
                "P" -> "Pending"
                "O" -> "Open"
                "C" -> "Completed"
                else -> "Unknown"
            }
        }
    }
}
