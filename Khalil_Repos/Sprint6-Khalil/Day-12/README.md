
# Welcome to your AWS Design and Development Python project!

This is a `Design Day 12` Task .



Task to do for this Project is:

1) Application Design ONLY - Create a design for the following application:

Tourism is usually the pillar industry of many countries because it has many benefits for improving
the national economy and political exchanges. Design a travel-oriented application that provides
customized and personalised service. The application should advise and help create a personalized
travel itinerary for tourists based on their purpose of visit (exploring, unwind, relaxation, adventure,
student trip, business), interests, number of days staying, and financial constraints. The application
should essentially help them filter attractions at their potential destination based on personal
information entered by them. For example, some tourists may be in Sydney to explore, while others
may be there to unwind and relax, while others might prefer a mix of both. Another example is that
some tourists might be interested in experiencing Japan's Cherry Blossom season. In this case, the
application should suggest the best time to visit Japan to experience this season is in the spring. It
should assist them by suggesting the best parks to visit based on their budget and the number of days
they are available, or in other words, their available time. Additionally, the application should assist in
choosing the best accommodation and all other necessary facilities (such as restaurants and
more) by recommending the best ones that fit their budget and were close to the parks.

### Description;
```
The design bascially start with user/traveler authentication,then thorugh front-end in this case we have API gateway, it will send 
requests ,mentioning his/her requirements for tour , then API gateway will trigger lambda which will basically sets all its requirements 
through already subscribed topic(SNS) to SQS Queue after that another lambda will be triggered which will basically fetch the Data From
Database and compare users requirements with already stored destination/tour-places information, one thing more the developer/manager will 
only connect with that data base to store new travel itinerary info for traveler, after lambda get values from Database it goes back 
through same resources and will show response to user.

```

### The AWS Resources will be used, listed as:

```
1) AWS Cognito
2) API GateWay
2) Lambda
3) SNS
4) SQS
5) RDS Database
6) Elastic Cache

```

Happy Coding!!!
