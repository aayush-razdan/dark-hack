var express = require("express");
var router = express.Router();
const { spawn } = require("child_process");

/* GET home page. */
router.get("/", function (req, res) {
  res.render("pages/home", { title: "DARK-HACK" });
});

/* GET form page. */
router.get("/form", function (req, res) {
  res.render("pages/form", { title: "DARK-HACK" });
});

/* POST form page. */
router.post("/form", function (req, res) {
  var dataToSend;

  // spawn new child process to call the python script
  const python = spawn("python", ["darkweb1.py", req.body.url]);

  // collect data from script
  python.stdout.on("data", function (data) {
    console.log("Pipe data from python script ...");
    // dataToSend = data.toString();
    dataToSend = data.toString();
    console.log(`stdout: ${dataToSend}`);
  });

  python.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  // in close event we are sure that stream from child process is closed
  python.on("close", (code) => {
    console.log(`child process close all stdio with code ${code}`);
    // send data to browser
    res.render("pages/crawler", {
      title: "DARK-HACK",
      test_string: dataToSend,
    });
  });

  // res.send("oops");
});

module.exports = router;
