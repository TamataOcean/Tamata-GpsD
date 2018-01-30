/*******************************************************************************
*  Code contributed to the webinos project
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*
*******************************************************************************/

var gpsd = require('node-gpsd');

var daemon = new gpsd.Daemon({
        program: 'gpsd',
        device: '/dev/ttyUSB0',
        verbose: true
});

//Start       
daemon.start(function() {
    var listener = new gpsd.Listener();

    listener.on('TPV', function (tpv) {
        console.log("----------- TPV --------------");
        console.log(tpv);
        console.log('Latitude: ' + tpv.lat);
        console.log('Longitude: ' + tpv.lon);
    });

    // parse is false, so raw data get emitted.
listener.on('raw', function(data) {
  console.log('-------------- ROW ------------- ');
  console.log(data);
});

    listener.connect(function() {
        listener.watch();
    });
});
