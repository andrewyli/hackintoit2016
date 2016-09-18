# ConnectMe

Created for Hack Into It @ Berkeley, Fall 2016

This is a prototype app to take in a user's LinkedIn and Facebook profiles, and generate a list of friends that can be used to ask for referrals to a job position within a company.

## Contributors

Andrew Li
Emma Hsu
Jackson Stogel
Jordan Hart
Ken Luy

## Project Goals and Model

Using linear regression on publicly available datasets such as that of the US Census, we created a model with the capacity to predict the stability and growth of an industry for a entry-level user of the application. Lasso was used in this process. Separately, use Facebook and LinkedIn API/CSV download/web crawlers to access friendlists and connections to get workplaces, and rate these (friend, job) pairs based on market viability. Return a sorted table of friends to get in contact with about finding a job based on a composite score.

## Further Work

- Figuring out a much faster and surefire way to bypass the restrictions on getting a user's friends/connections, given that the two services of Facebook and LinkedIn fail to provide adequate APIs
- Potentially using more complicated modeling such as random forest regression in the future
- Given a faster and more reliable search method, provide true networking reach and allow access to friends of friends for cross-referral
