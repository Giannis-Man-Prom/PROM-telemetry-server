To fix the front end:
1. Change .envexample to .env
2. Run "npm install" to install dependencies
3. The purpose is to run "npm run build" but it throws errors
4. To alleviate those errors:
    a. Go to the "tscongig.ts", add below the "skipLibCheck" '"allowJs":true,' and delete the linting section
    b. In App.vue in line 13: "@/types/live_telemetry.ts"; -> "./types/live_telemetry.ts";
    c. In App.vue in line 14: "@/types/socketIO.types.ts" -> "./types/socketIO.types.ts";
    d. In CustomBarChart.vue line 10: -> import telemetry_data_obj from '../App.vue';
    e. In CustomLineChart.vue line 59: -> data.push(items.value[0][0]);
    f. For the errors (3) " Argument of type 'VehicleTelemetry_data' is not assignable to parameter of type 'string' " do: telemetry_data.data as unknown as string
    g. In ShowCustomCharts.vue in line 42: -> import {linechartItems, VehicleTelemetry_data} from "../types/live_telemetry.ts";
    h. For the errors (2) " Conversion of type 'undefined[]' to type 'variableContainer' may be a mistake because neither type sufficiently overlaps with the other. If this was intentional, convert the expression to 'unknown' first. " do: ... [] as unknown as ...

To fix the backend:
1. Change the .env in the telemetry-ui-server-develop
2. Go into the file live_telemetry_class.py and line 58 and do: ->for port in self.ports if port.serial_number == '3086377C3233':