var express = require("express");
var router = express.Router();
var request = require("request");
var aws = require("aws-sdk");
var ses = new aws.SES({ region: "eu-north-1" });

/* GET home page. */
router.get("/", function (req, res) {
  res.render("pages/home", { title: "DARK-HACK" });
});

/* GET form page. */
router.get("/form", function (req, res) {
  res.render("pages/form", { title: "DARK-HACK" });
});

/* GET form page. */
router.get("/tableData", function (req, res) {
  res.render("pages/tableData", { title: "DARK-HACK" });
});
/* POST form page. */
router.post("/form", function (req, res) {
  // res.send(JSON.stringify(req.body));
  console.log(req.body);
  options = {
    uri: `http://127.0.0.1:5000/flask/crawl?url=${req.body.url}`,
    // json: req.body.url,
    method: "POST",
    headers: { "Content-type": "application/json", Accept: "text/plain" },
  };
  request.post(options, function (error, response, body) {
    console.error("error:", error); // Print the error
    console.log("statusCode:", response && response.statusCode); // Print the response status code if a response was received
    console.log("body:", body); // Print the data received

    // res.send(body); //Display the response on the website
    res.render("pages/crawler-output", {
      title: "DARK-HACK",
      test_string: body,
    });
  });
});

/* GET scrape body form page. */
router.get("/scrape-body", function (req, res) {
  res.render("pages/scrape-body", { title: "DARK-HACK" });
});

/* POST scrabe body form page. */
router.post("/scrape-body", function (req, res) {
  payload = "";
  // res.send(JSON.stringify(req.body));
  console.log(req.body);
  options = {
    uri: `http://127.0.0.1:5000/flask/scrape_body?url=${req.body.scrapeurl}`,
    // json: req.body.url,
    method: "POST",
    headers: { "Content-type": "application/json", Accept: "text/plain" },
  };
  request.post(options, function (error, response, body) {
    console.error("error:", error); // Print the error
    console.log("statusCode:", response && response.statusCode); // Print the response status code if a response was received
    console.log("body:", body); // Print the data received
    payload = payload.concat(body);
    //now running the classification on this data
    request.post(
      {
        uri: `http://127.0.0.1:5000/flask/porns?`,
        headers: { "Content-type": "application/json", Accept: "text/plain" },
        form: { text: body },
      },
      function (e1, r1, b1) {
        console.error("error1:", e1);
        console.log("statusCode1:", r1 && r1.statusCode);
        console.log("body1:", b1);
        payload = payload.concat(b1);
      }
    );

    request.post(
      {
        uri: `http://127.0.0.1:5000/flask/drugs?`,
        headers: { "Content-type": "application/json", Accept: "text/plain" },
        form: { text: body },
      },
      function (e2, r2, b2) {
        console.error("error2:", e2);
        console.log("statusCode2:", r2 && r2.statusCode);
        console.log("body2:", b2);
        payload = payload.concat(b2);
      }
    );

    request.post(
      {
        uri: `http://127.0.0.1:5000/flask/intelligence?`,
        headers: { "Content-type": "application/json", Accept: "text/plain" },
        form: { text: body },
      },
      function (e3, r3, b3) {
        console.error("error3:", e3);
        console.log("statusCode3:", r3 && r3.statusCode);
        console.log("body3:", b3);
        payload = payload.concat(b3);
      }
    );

    console.log(payload);
    // res.send(body); //Display the response on the website
    res.render("pages/scrape-body-output", {
      title: "DARK-HACK",
      test_string: payload,
    });
  });
});

router.get("/requestPage", function (req, res) {
  res.render("pages/raiseRequest", { title: "DARK-HACK" });
});

router.post("/email", function (req, res) {
  const { ip, carrier, issue } = req.body;
  console.log("req", req.body);
  sesTest("dikshaasharma2702@gmail.com", ip, carrier, issue)
    .then((val) => {
      console.log("got this back", val);
      res.send("Successfully Sent Email");
    })
    .catch((err) => {
      res.send("/error");

      console.log("There was an error!", err);
    });
});

function sesTest(emailTo, ip, carrier, issue) {
  var params = {
    Destination: {
      ToAddresses: [emailTo],
    },
    Message: {
      Body: {
        Text: {
          Data:
            "IP ADDRESS/PHONE NUMBER: " +
            ip +
            "\n " +
            "CARRIER: " +
            carrier +
            "\n " +
            "ISSUE: " +
            issue,
        },
      },

      Subject: { Data: "New Request" },
    },
    Source: "aayuisback@gmail.com",
  };

  return ses.sendEmail(params).promise();
}

module.exports = router;
