# Testing of Hotel Booking System

## Functional Testing

### All pages tested

| Test Case             | Description                                                 | Steps                                                                                                                                                       | Expected Outcome                                                                              |
|-----------------------|-------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| Register New User     | Verify that new users can register successfully.           | 1. Access the registration page. 2. Fill in the registration form with valid user details. 3. Submit the form. 4. Verify that the user is redirected to the login page with a success message indicating successful registration. | New user is registered successfully and redirected to the login page with a success message. |
| Login                 | Verify that registered users can log in successfully.       | 1. Access the login page. 2. Enter valid login credentials (username and password). 3. Submit the form. 4. Verify that the user is redirected to the view hotels page with a success message indicating successful login. | User is logged in successfully and redirected to the view hotels page with a success message. |
| Logout                | Verify that logged-in users can log out successfully.       | 1. Access the logout functionality (e.g., logout link or button). 2. Click on the logout functionality. 3. Verify that the user is redirected to the common viewhotels page with a success message indicating successful logout. | User is logged out successfully and redirected to the common viewhotels page with a success message. |
| Password Reset        | Verify that users can reset their password successfully.    | 1. Access the password reset page. 2. Enter the registered your user name and Enter a new password. 3. Submit the form. 4. Verify that the user is redirected to the login page with a success message indicating successful password reset. | User's password is reset successfully and redirected to the login page with a success message. |
| Unsubscribe           | Verify that users can unsubscribe or delete their account successfully. | 1. Access the unsubscribe page. 2. Confirm the action to delete the account. 3. Verify that the account is deleted successfully. 4. Attempt to log in with the deleted account credentials. | User account is deleted successfully and cannot log in with the deleted account credentials. |
| Add Hotel             | Verify that hotel managers can add a new hotel successfully. | 1. Access the "Add Hotel" page in the hotel manager add hotel. 2. Fill in the required hotel details. 3. Submit the form. 4. Verify that the new hotel is added to the system. 5. Attempt to view the added hotel details. | New hotel is added successfully and can be viewed with the added hotel details. |
| Edit Hotel            | Verify that hotel managers can edit hotel details successfully. | 1. Access the "Edit Hotel" page for a specific hotel in the hotel manager view hotels. 2. Modify the hotel details. 3. Submit the form. 4. Verify that the hotel details are updated in the system. 5. Attempt to view the updated hotel details. | Hotel details are updated successfully and can be viewed with the updated hotel details. |
| Delete Hotel          | Verify that hotel managers can delete a hotel successfully. | 1. Access the "Delete Hotel" functionality for a specific hotel in the hotel manager view hotels. 2. Confirm the action to delete the hotel. 3. Verify that the hotel is deleted from the system. 4. Attempt to view the deleted hotel details. | Hotel is deleted successfully and cannot be viewed with the deleted hotel details. |
| Book Hotel            | Verify that clients can book a hotel successfully.         | 1. Access the "Book Hotel" page for a specific hotel. 2. Fill in the booking details (check-in date, check-out date, number of guests). 3. Submit the form. 4. Verify that the booking is confirmed and added to the system. 5. Attempt to view the booked hotel details on client dashboard. | Hotel is booked successfully and can be viewed with the booked hotel details on client dashboard.. |
| Reschedule Booking    | Verify that clients can reschedule their booking successfully. | 1. Access the "Reschedule Booking" functionality for a specific booking. 2. Modify the booking details (check-in date, check-out date). 3. Submit the form. 4. Verify that the booking is rescheduled and updated in the system. 5. Attempt to view the updated booking details. | Booking is rescheduled successfully and can be viewed with the updated booking details. |
| Cancel Booking        | Verify that clients can cancel their booking successfully. | 1. Access the "Cancel Booking" functionality for a specific booking. 2. Confirm the action to cancel the booking. 3. Verify that the booking is cancelled and removed from the system. 4. Attempt to view the cancelled booking details. | Booking is cancelled successfully and cannot be viewed with the cancelled booking details. |
| Rate Experience       | Verify that clients can rate their booking experience successfully. | 1. Access the "Rate Experience" functionality for a specific booking. 2. Select a rating for the experience. 3. Submit the rating. 4. Verify that the rating is added to the booking and updated in the system. 5. Attempt to view the updated booking details. | Experience is rated successfully and can be viewed with the updated booking details in the view hotels page at specific hotel. |
| View User Ratings     | Verify that clients can view their ratings for previous bookings. | 1. Access the "View User Ratings" page in the client dashboard. 2. Verify that the ratings for previous bookings are displayed correctly. | Ratings for previous bookings are displayed correctly in the client dashboard. |
| Manage Bookings       | Verify that hotel managers can manage their hotel bookings successfully. | 1. Access the "Manage Bookings" page in the hotel manager dashboard. 2. Verify that the list of bookings for the hotel is displayed correctly. 3. Attempt to perform various actions such as view bookings. | Hotel manager can view bookings for the hotel successfully. |
| Generate Excel Report | Verify that hotel managers can generate an Excel report of their hotel bookings successfully. | 1. Access the "Generate Excel Report" functionality in the hotel manager manage bookings. 2. Select the desired parameters for the report. 3. Generate the report. 4. Verify that the Excel report is downloaded successfully. | Excel report of hotel bookings is downloaded successfully. |

### Responsiveness

All pages have been tested for responsiveness with Google Chrome Developer Tools on screens from 320px, making sure the content adjusts correctly on all screen sizes.

On physical device, it has been tested on iPhone 13 in vertical and horizontal orientation.

### Browsers compatibility

The website has been tested in the following browsers on desktop, without finding any significant problems:

* Chrome
* Safari
* Firefox
* Opera
* Edge

### Fixed Bugs

| Form / View               | Bug                                                                                                           | Solution                                                                                                                         |
|---------------------------|---------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| CustomRegistrationForm   | The form does not handle cases where the provided username or email already exists, potentially leading to duplicate user registrations.      | Integrate form validation within the `register_view` to verify if a user with the provided username or email already exists in the database. If a user with the same username or email exists, display an appropriate error message informing the user that the username or email is already taken. Prompt the user to choose a different one during registration. |
| AuthenticationForm       | The form does not provide adequate error feedback for unsuccessful login attempts, potentially confusing users. | Enhance the error handling mechanism in the `login_view` to provide descriptive error messages indicating the reason for login failure (e.g., incorrect username, incorrect password). This will help users understand why their login attempt failed and guide them on how to proceed (e.g., verify username, reset password). |
| YourBookingForm          | The form does not handle cases where the booking dates are invalid (e.g., backdated check-in dates, check-out dates before check-in dates), leading to inconsistent or erroneous bookings. | Implement form validation to check the validity of booking dates entered by the user. Validate that the check-out date is not before the check-in date and that neither the check-in nor check-out dates are backdated. Provide appropriate error feedback if the entered dates are invalid, guiding the user to input correct date ranges. |
| ModifyBookingForm        | The form does not handle cases where the provided booking ID is invalid or does not exist, potentially leading to errors during booking modification attempts. | Implement validation to check if the provided booking ID exists in the database before processing any modification requests. If the booking ID is invalid or does not exist, display an error message indicating that the specified booking does not exist, prompting the user to provide a valid booking ID for modification. |
| CommentForm              | The form does not handle cases where the submitted comment text exceeds the maximum allowed length, potentially causing issues during comment submission. | Add validation to restrict the length of the comment text to the maximum allowed length specified for comments. If the submitted comment text exceeds the maximum length, display an error message indicating that the comment text is too long, prompting the user to shorten the comment. |
| RatingForm               | The form does not handle cases where the submitted rating value is outside the valid range (e.g., not within the specified rating scale), leading to inconsistent or erroneous ratings. | Implement validation to ensure that the submitted rating value falls within the valid range specified for ratings (e.g., between 1 and 5). If the submitted rating value is outside the valid range, display an error message indicating that the rating value is invalid, prompting the user to select a rating within the specified range. |
| register_view            | The view does not handle cases where the provided username or email already exists, potentially leading to duplicate user registrations. | Integrate form validation within the `register_view` to verify if a user with the provided username or email already exists in the database. If a user with the same username or email exists, display an appropriate error message informing the user that the username or email is already taken. Prompt the user to choose a different one during registration. |
| login_view               | The view does not provide adequate error feedback for unsuccessful login attempts, potentially confusing users. | Enhance the error handling mechanism in the `login_view` to provide descriptive error messages indicating the reason for login failure (e.g., incorrect username, incorrect password). This will help users understand why their login attempt failed and guide them on how to proceed (e.g., verify username, reset password). |
| CustomPasswordResetConfirmView | The view does not correctly validate the reset token against the token stored in the database for the corresponding user's email. | Update the `CustomPasswordResetConfirmView` to verify the reset token against the token stored in the database for the corresponding user's email. If the token matches, allow the user to reset their password; otherwise, display an error message indicating an invalid token. |
| generate_excel           | The view does not handle cases where there are no bookings data available, resulting in potential errors during Excel file generation. | Implement a check within the `generate_excel` view to verify if there are bookings data available before attempting to generate the Excel file. If there are no bookings data available, handle the situation gracefully by returning an appropriate response (e.g., render a template with a message indicating no data available for export). |
| view_booking_details    | The view does not handle cases where the specified booking ID does not exist in the database, potentially resulting in errors when attempting to view non-existent bookings. | Implement error handling in the `view_booking_details` view to check if the provided booking ID exists in the database. If the booking ID does not exist, return an appropriate error message indicating that the specified booking does not exist, guiding the user to provide a valid booking ID for viewing. |

### Unfixed Bugs

When delete the booking the related rating and comments not deleting accordingly

*-* **Bug:** Currently, when a booking is deleted from the system, the related ratings and comments are not automatically deleted. This inconsistency can lead to data inconsistencies and clutter in the database, as orphaned ratings and comments remain even after the booking has been removed.

  *-* **Description:** When a booking is deleted, the related ratings and comments should also be deleted to maintain data consistency and ensure a clutter-free database.

  *-* **Impact:**
    *-* Data Inconsistency: Orphaned ratings and comments remain in the database, leading to data inconsistency and potential issues with data integrity.
    *-* Cluttered Database: Accumulation of orphaned ratings and comments over time can clutter the database, impacting system performance and manageability.

  *-* **Steps to Reproduce:**
    1. Create a booking in the system.
    2. Add ratings and comments related to the created booking.
    3. Delete the booking from the system.
    4. Observe that the related ratings and comments are not deleted along with the booking.

  *-* **Expected Behavior:** When a booking is deleted from the system, all related ratings and comments associated with that booking should also be deleted to maintain data consistency and ensure a clutter-free database.

  *-* **Proposed Solution:** Implement a cascading delete mechanism in the database schema or update the deletion logic in the system to automatically delete related ratings and comments when a booking is deleted.

  *-* **Severity:** High

  *-* **Priority:** Medium

## Unit Testing

Unit tests have been implemented to test basic functionality of models, forms and views.

![Automation Tests](hotels_booking/documentation/automation_tests.png)

