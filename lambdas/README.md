# Info

This directory holds all the code used in the assignment.

## Container

There's one "super-container" for all lambdas in this project, in practice this means that you can use simply override
`CMD` call through the web UI, in order to invoke a specific lambda without having to track per-lambda containers.
Yes, it's not ideal and not really in the spirit of containerisation, but then, again this is for a school project, so
it doesn't really matter.
