# Eveready API
##  A SUUUUPER simple Flask container to scrape data from [app.evereadysolarstorage.com](https://app.evereadysolarstorage.com) and re-serve it with a RESTful API
### Built for use with Home Assistant


## REQUIREMENTS

Python Library Dependencies are listed in `requirements.txt`

you MUST define 3 Environment variables:
- EVEREADY_USERNAME
  - The username you use to sign into the Eveready Energy Vault App or [Web Portal](https://app.evereadysolarstorage.com).
  - e.g. `me@home.com`
- EVEREADY_PASSWORD
  - Password for the above account
- EVEREADY_SERIAL
  - The Serial Number of your Eveready Inverter
    - e.g. `ASS0123J4567E89012` (not a real serial number)

## Building the Docker Image from the Dockerfile

1. Clone the repository to your environment: `git clone https://github.com/HiveMindAutomation/EvereadyAPI.git`
2. Change Directory to the newly created Folder: `cd EvereadyAPI`
3. Build the Docker Image: `docker build -t hivemindautomation/evereadyapi .` (you can replace `hivemindautomation/evereadyapi` with your own tags if you want)

## ALTERNATIVE - pull the image from Docker Hub

1. Pull the Docker image from Docker hub directly:
   1. `docker pull djstuey/evereadyapi:latest`

## Start the Container:


1. Build or pull the Docker Image
2. Start the container - remember, port 5000 needs to be exposed and you need to set environment variables. e.g:
```bash
docker run \
-p 5000:5000 \                                  # Open port 5000.
-e EVEREADY_USERNAME="me@home.com" \            # Set Username Environment Variable
-e EVEREADY_PASSWORD="changeme123#" \           # Set Password Environment Variable
-e EVEREADY_SERIAL="ASS0123J4567E89012" \       # Set Serial Number Environment Variable
djstuey/evereadyapi:latest
```

## Testing the service is working:

To test if the service is working, you can navigate to [http://127.0.0.1:4999/eveready/battery](http://127.0.0.1:5000/eveready/battery).
The service should return valid JSON on a single line:
```JSON
{"backupLoadPower":0.0,"batCapcity":100.0,"batConsumpDirection":0,"batConsumpPower":0.0,"batCurr":0.0,"batEnergyPercent":16.0,"batGridDirection":0,"batGridPower":0.0,"batteryDirection":0,"batteryPower":0.0,"dataTime":1745843400000,"gridChargePower":0.0,"gridConsumpDirection":0,"gridConsumpPower":0.0,"gridDirection":-1,"gridPower":1244.0,"inputOutputPower":0.0,"isAlarm":0,"isOnline":1,"mark":1,"outPutDirection":1,"pvChargeDirection":0,"pvChargePower":0.0,"pvConsumpDirection":0,"pvConsumpPower":0.0,"pvDirection":1,"pvGridDirection":0,"pvGridPower":0.0,"pvPower":7.0,"runningState":1,"solarPower":5.18,"totalLoadPower":1251.0,"updateDate":1745835941000}
```
Formatted, it should look like this:
```JSON
{
    "backupLoadPower":0.0,
    "batCapcity":100.0,
    "batConsumpDirection":0,
    "batConsumpPower":0.0,
    "batCurr":0.0,
    "batEnergyPercent":16.0,
    "batGridDirection":0,
    "batGridPower":0.0,
    "batteryDirection":0,
    "batteryPower":0.0,
    "dataTime":1745843400000,
    "gridChargePower":0.0,
    "gridConsumpDirection":0,
    "gridConsumpPower":0.0,
    "gridDirection":-1,
    "gridPower":1244.0,
    "inputOutputPower":0.0,
    "isAlarm":0,
    "isOnline":1,
    "mark":1,
    "outPutDirection":1,
    "pvChargeDirection":0,
    "pvChargePower":0.0,
    "pvConsumpDirection":0,
    "pvConsumpPower":0.0,
    "pvDirection":1,
    "pvGridDirection":0,
    "pvGridPower":0.0,
    "pvPower":7.0,
    "runningState":1,
    "solarPower":5.18,
    "totalLoadPower":1251.0,
    "updateDate":1745835941000
}
```

## Data Fields
I believe the fields map - roughly - to the following table. The Mappings may not be corrrect.

| Sensor Name                         | JSON Key               | Value Type       | Mappings / Units                         | Description                                                             |
| ----------------------------------- | ---------------------- | ---------------- | ---------------------------------------- | ----------------------------------------------------------------------- |
| Eveready Backup Load Power          | `backupLoadPower`      | Number (float)   | W – Watts                                | Instantaneous power supplied to the emergency/backup load circuit. If this circuit is not wired, this should always show 0.    |
| Eveready Battery Capacity           | `batCapcity`           | Number (float)   | Ah – Ampere Hours                        | Nominal battery capacity. Used for estimating full capacity.            |
| Eveready Battery to Load Direction  | `batConsumpDirection`  | Integer (0/1)    | 1 = Discharging to home; 0 = Not         | Indicates whether the battery is actively powering household loads.     |
| Eveready Battery to Load Power      | `batConsumpPower`      | Number (float)   | W – Watts                                | Power being drawn from the battery by household loads.                  |
| Eveready Battery Current            | `batCurr`              | Number (float)   | A – Amps                                 | Real-time battery current. Negative = charging, positive = discharging. |
| Eveready Battery State of Charge    | `batEnergyPercent`     | Number (float)   | %                                        | % Charge remaining in the battery (0–100%).                               |
| Eveready Battery to Grid Direction  | `batGridDirection`     | Integer (0/1)    | 1 = Exporting to grid; 0 = Not           | Indicates if the battery is feeding power into the grid.                |
| Eveready Battery to Grid Power      | `batGridPower`         | Number (float)   | W – Watts                                | Power from the battery being sent to the grid.                          |
| Eveready Battery Direction          | `batteryDirection`     | Integer (-1/0/1) | -1 = Charging; 0 = Idle; 1 = Discharging | Indicates net power flow direction into or out of the battery.          |
| Eveready Battery Power              | `batteryPower`         | Number (float)   | W – Watts                                | Total output power of the battery (sum of all destinations).            |
| Eveready Data Timestamp             | `dataTime`             | Epoch (ms)       | Formatted timestamp                      | Local time of when the data was measured.                               |
| Eveready Grid Charge Power          | `gridChargePower`      | Number (float)   | W – Watts                                | Grid power going into battery for charging.                             |
| Eveready Grid Consumption Direction | `gridConsumpDirection` | Integer (0/1)    | 1 = Importing from grid; 0 = Not         | Whether the home is drawing power from the grid.                        |
| Eveready Grid Consumption Power     | `gridConsumpPower`     | Number (float)   | W – Watts                                | Power being pulled from grid to meet demand.                            |
| Eveready Grid Direction             | `gridDirection`        | Integer (0/1)    | 1 = Exporting; 0 = Importing             | Indicates net flow direction with respect to the grid.                  |
| Eveready Grid Power                 | `gridPower`            | Number (float)   | W – Watts                                | Magnitude of power exchange with the grid.                              |
| Eveready Input/Output Power         | `inputOutputPower`     | Number (float)   | W – Watts                                | Net system power flow (can be used to estimate charge/discharge).       |
| Eveready Alarm Status               | `isAlarm`              | Integer (0/1)    | 1 = Alarm active; 0 = No alarm           | Indicates if any system alarms or faults are present.                   |
| Eveready Online Status              | `isOnline`             | Integer (0/1)    | 1 = Online; 0 = Offline                  | Whether the system is currently online and reporting data.              |
| Eveready Data Mark                  | `mark`                 | Integer          | Diagnostic/undefined                     | Possibly used internally.                                               |
| Eveready Output Direction           | `outPutDirection`      | Integer (0/1)    | 1 = Supplying power; 0 = Absorbing       | Indicates general output/input status of the system.                    |
| Eveready PV Charge Direction        | `pvChargeDirection`    | Integer (0/1)    | 1 = PV charging battery; 0 = Not         | Whether solar is currently charging the battery.                        |
| Eveready PV Charge Power            | `pvChargePower`        | Number (float)   | W – Watts                                | Power from PV being used to charge the battery.                         |
| Eveready PV Consumption Direction   | `pvConsumpDirection`   | Integer (0/1)    | 1 = PV powering house; 0 = Not           | Whether PV is supplying household loads.                                |
| Eveready PV Consumption Power       | `pvConsumpPower`       | Number (float)   | W – Watts                                | Amount of solar power being directly consumed by the house.             |
| Eveready PV Direction               | `pvDirection`          | Integer (0/1)    | 1 = PV producing; 0 = Not                | Whether the PV system is currently generating power.                    |
| Eveready PV to Grid Direction       | `pvGridDirection`      | Integer (0/1)    | 1 = PV exporting to grid; 0 = Not        | If any solar is being exported to the grid.                             |
| Eveready PV to Grid Power           | `pvGridPower`          | Number (float)   | W – Watts                                | How much PV-generated power is being sent to the grid.                  |
| Eveready PV Power                   | `pvPower`              | Number (float)   | W – Watts                                | Total real-time output from the PV panels.                              |
| Eveready Running State              | `runningState`         | Integer          | 1 = Running (others undocumented)        | General operational state of the battery system.                        |
| Eveready Solar Power                | `solarPower`           | Number (float)   | kWh – kilowatt-hours                     | Total solar energy generated (likely for the day).                      |
| Eveready API Status                 | `status`               | String           | "success", "error", etc.                 | Whether the API request was successful.                                 |
| Eveready Response Type              | `type`                 | Integer          | 2 = Battery system (in examples)         | May represent system type/device type.                                  |
| Eveready Last Update Timestamp      | `updateDate`           | Epoch (ms)       | Formatted timestamp                      | Last update time as reported by the battery system.                     |


## Adding Sensors to Home Assistant:

The included sensor.yaml contains all you need to add your configuration.yaml in Home Assistant to map each JSON key to an entity.  

## Troubleshooting
  
### A Common issue:


### Problem:
Port 5000 is in use:  
`Error response from daemon: Ports are not available`  
or  
`bind: address already in use`

### Recommended Solution:
Change the external port mapping. The left⬅️ side of the `:` after `-p` in the run command is the external port number. Try changing it to something other than 5000.
4999 works most often for me.
Port 5000 is commonly consumed by the Airplay Service on macOS devices.

## Known Issues:

- SSL Validation for pulling from Eveready is currently disabled. I was getting SSL errors and just needed to get something working... it's on the TODO list

## Other TODOs

- Might be nice to build a real web front-end and display the data nicely
- Undecided if I should be breaking some of the JSON Keys off into their own endpoints or grouping them in some way. 
  - i.e. grouping all the `pv` values in one endpoint, `battery` values in another, and `grid` in yet another... this might just help to keep the JSON output tidier
- 