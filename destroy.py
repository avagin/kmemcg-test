import os, time, sys, signal
memcg_test_dir = os.path.normpath(sys.argv[1])
memcg_dir = os.path.dirname(memcg_test_dir)
print memcg_dir

# Create and move into a test group
os.mkdir(memcg_test_dir)
open(memcg_test_dir + "/memory.kmem.limit_in_bytes", "w").write("1024000000")
open(memcg_test_dir + "/tasks", "w").write(str(os.getpid()))

# Open a test file
tfd = open("/proc/mounts")
tfd.close()

# Open in a second time, because the first one is not accounted
tfd = open("/proc/mounts")

# Move back intho the root group
cf = open(memcg_dir + "/tasks", "w")
cf.write(str(os.getpid()))
cf.close()

# Open slabinfo to monitor which caches will be destroyed.
fd = open(memcg_test_dir + "/memory.kmem.slabinfo")
print fd.read()

# Destroy the test group.
os.rmdir(memcg_test_dir)
time.sleep(1)

fd.seek(0)
print fd.read()
tfd.close()

# The filp slab must be destroyed.
for i in xrange(10):
	fd.seek(0)
	out = fd.read()
	print out
	if "filp" in out:
		time.sleep(1)
		continue
	print "PASS"
	sys.exit(0)
print "FAIL"
sys.exit(1);

