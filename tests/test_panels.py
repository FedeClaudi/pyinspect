import pyinspect as pi


def test_panels():
    pi.message("panel", "this is a test")
    pi.warn("warn", "this is a test")
    pi.ok("ok", "this is a test")
    pi.error("error", "this is a test")

    pi.error("error")


def test_report():
    pi.whats_pi()  # tests both Report and Nested Report
