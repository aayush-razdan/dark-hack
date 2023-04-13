var express = require("express");
var router = express.Router();

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

/* POST form page. */
router.post("/form", function (req, res) {
  res.send(JSON.stringify(req.body));
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
