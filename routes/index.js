var express = require("express");
var router = express.Router();

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

module.exports = router;
