✅ ================== 5. Optional Features to Add Later =============================

✅ Mileage Calculations. 

✅ Totals in services offered. 

✅  Email/SMS Notifications to fleet Manager, Driver, and Requestor
 i.e:
 * Driver is notified when a car is allocated, when a request for trip is assigned etc, 
 * Manager is notified when a car is returned, when there is a pending request for approval etc, 
 * Requestor is notified when a car is allocated for trip etc
 and other required or necessary notifications to respective individuals in the system. 

✅  Export reports all trip logs with alert summaries and all other required info in (CSV, PDF) for Printing reports. 


Chart views (speed trends, fuel drop, etc.)


Final Project report. 

🛡️ Bonus Suggestions for Professionalism
🔐 You can restrict viewing alerts to FleetManagers using Django groups.

📩 Use email notification via Django’s send_mail() in the signal if needed.

📊 Add a dashboard widget to count/display unread alerts.

Would you like me to help:

Add email alerts in this signal?

Create a notification bell icon for alerts on the navbar?

Build CSV download or filtering for alerts?




Add the following views and URLs (if not already):

assigned_trips

driver_profile

trip_history


@login_required
def trip_history(request):
    try:
        driver = Driver.objects.get(user=request.user)
    except Driver.DoesNotExist:
        messages.error(request, "No driver profile found for this user.")
        return redirect('home')

    trips = Request.objects.filter(
        vehicle=driver.vehicle,
        request_status='C'
    ).select_related('vehicle', 'requestor')

    for trip in trips:
        if trip.mileage_at_return and trip.mileage_at_assignment:
            trip.mileage_used = trip.mileage_at_return - trip.mileage_at_assignment
        else:
            trip.mileage_used = None

    return render(request, 'fleetApp/driver/trip_history.html', {'trips': trips})



@login_required
def return_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    
    # Ensure only the assigned driver can return
    try:
        driver = Driver.objects.get(user=request.user)
        if driver.vehicle != vehicle:
            messages.error(request, "You are not assigned to this vehicle.")
            return redirect('assigned_trips')
    except Driver.DoesNotExist:
        messages.error(request, "Driver profile not found.")
        return redirect('home')

    if request.method == "POST":
        form = VehicleReturnForm(request.POST)
        if form.is_valid():
            mileage_at_return = form.cleaned_data['mileage_at_return']

            # Update the request object
            request_obj = Request.objects.filter(vehicle=vehicle, request_status="O").first()
            if request_obj:
                request_obj.mileage_at_return = mileage_at_return
                request_obj.request_status = "C"
                request_obj.time_of_return = timezone.now()
                request_obj.save()

            # Update vehicle and driver
            vehicle.status = 'Available'
            vehicle.mileage = mileage_at_return
            vehicle.save()

            driver.vehicle = None
            driver.save()

            messages.success(request, "Vehicle returned and trip completed.")
            return redirect('trip_history')
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = VehicleReturnForm()

    return render(request, 'fleetApp/vehicle/return_vehicle.html', {'vehicle': vehicle, 'form': form})
