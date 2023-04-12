var express = require("express");
var router = express.Router();

/* GET home page. */
router.get("/", function (req, res) {
  res.render("pages/home", { title: "DARK-HACK" });
});

module.exports = router;
