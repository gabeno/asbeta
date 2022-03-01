#### Decisions considered

1. Use of DFS since problem closely mimics processing a tree.
2. Consider only working with python objects for now. Depending on usage another desired format may be used eg JSON
3. Usage of dev dependencies to help with formatting, linting and testing


#### Desired Improvements

1. Expose this as a service within an ecosystem of services:
   a. Via an endpoint
   b. As an internal dependency library
2. More flexibility on the code to enable it handle schema modifications since from experience schema evolves over time.
3. Handle concurrent updates on documents from different clients, some options in mind being
   a. adopt async/await patterns for update
   b. use locks to control updates


#### Comments

Working on the problem was fun and engaging. I felt it touched on various aspects of software development.

To run tests do `pytest .` in the root folder.