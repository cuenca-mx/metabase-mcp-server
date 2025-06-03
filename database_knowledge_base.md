# Example: Database Knowledge Base Template

> This is a generic example for a data science assistant using Metabase and Redshift. **You must adapt this file with your own database, table, and business logic information before using it in production.**

## Guidelines
- Use Metabase to answer user data requests.
- Always check existing questions (cards) for examples before writing new queries.
- Run queries to verify current table columns and relationships.
- Convert all dates to UTC if needed.
- Test every question before saving to ensure it returns expected results.

## Example Database (Redshift)
- `database_id=2`, engine: Redshift, name: ExampleTravelDB

## Example Tables (Travel Agency)
- **customers**: id, first_name, last_name, email, created_at
- **bookings**: id, customer_id, trip_id, booking_date, status, total_amount
- **trips**: id, destination, start_date, end_date, price
- **payments**: id, booking_id, payment_date, amount, payment_method
- **agents**: id, name, email, phone
- **reviews**: id, customer_id, trip_id, rating, comment, review_date

## Additional Notes
- For customer activity profiles: calculate the average total_amount of bookings in the customer's first month.
- Exclude cancelled bookings when analyzing customer history.

---
**Replace all table/field names and business rules above with those relevant to your own project.**