# Farmers Market

This application will allow you to checkout a customer for the Farmer's Market

## To run:
Make sure Docker is installed.
In a PowerShell window, build and run the application by navigating to this folder and typing:

`
docker build -t farmersmarket .
`

After the file has successfully built, run the app by typing:

`
docker run -it farmersmarket
`

To stop the application, take note of the code that is produced from the docker run command, or type:
 `
 docker stats
 `

 This will give you the 12-digit container that you need to stop. Take that number and type in:

 `docker stop <12-digit code>
`