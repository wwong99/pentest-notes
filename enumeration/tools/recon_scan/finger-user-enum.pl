#!/usr/bin/perl -w
# finger-user-enum - Brute Force Username via Finger Service
# Copyright (C) 2006 pentestmonkey@pentestmonkey.net
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as 
# published by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# This tool may be used for legal purposes only.  Users take full responsibility
# for any actions performed using this tool.  If these terms are not acceptable to 
# you, then do not use this tool.
# 
# You are encouraged to send comments, improvements or suggestions to
# me at finger-user-enum@pentestmonkey.net
#
# This program is derived from dns-grind v1.0 ( http://pentestmonkey.net/tools/dns-grind )

use strict;
use Socket;
use IO::Handle;
use IO::Select;
use IO::Socket::INET;
use Getopt::Std;
$| = 1;

my $VERSION        = "1.0";
my $debug          = 0;
my @child_handles  = ();
my $verbose        = 0;
my $max_procs      = 5;
my $finger_port    = 79;
my @usernames      = ();
my @hosts          = ();
my $recursive_flag = 1;
my $relayserver    = undef;
my $query_timeout  = 5;
my $start_time     = time();
my $end_time;
my $kill_child_string = "\x00";
$SIG{CHLD} = 'IGNORE'; # auto-reap
my %opts;
my $usage=<<USAGE;
finger-user-enum v$VERSION ( http://pentestmonkey.net/tools/finger-user-enum )

Usage: finger-user-enum.pl [options] ( -u username | -U file-of-usernames ) ( -t host | -T file-of-targets )

options are:
        -m n     Maximum number of resolver processes (default: $max_procs)
	-u user  Check if user exists on remote system
	-U file  File of usernames to check via finger service
	-t host  Server host running finger service
	-T file  File of hostnames running the finger service
	-r host  Relay.  Intermediate server which allows relaying of finger requests.
	-p port  TCP port on which finger service runs (default: $finger_port)
	-d       Debugging output
	-s n     Wait a maximum of n seconds for reply (default: $query_timeout)
	-v       Verbose
	-h       This help message

Also see finger-user-enum-user-docs.pdf from the finger-user-enum tar ball.

Examples:

\$ finger-user-enum.pl -U users.txt -t 10.0.0.1
\$ finger-user-enum.pl -u root -t 10.0.0.1
\$ finger-user-enum.pl -U users.txt -T ips.txt

USAGE

getopts('m:u:U:t:T:p:r:ds:vh', \%opts);

# Print help message if required
if ($opts{'h'}) {
	print $usage;
	exit 0;
}

my $username       = $opts{'u'} if $opts{'u'};
my $username_file  = $opts{'U'} if $opts{'U'};
my $host           = $opts{'t'} if $opts{'t'};
my $host_file      = $opts{'T'} if $opts{'T'};
my $file           = $opts{'f'} if $opts{'f'};

$query_timeout  = $opts{'s'} if $opts{'s'};
$relayserver    = $opts{'r'} if $opts{'r'};
$max_procs      = $opts{'m'} if $opts{'m'};
$finger_port    = $opts{'p'} if $opts{'p'};
$verbose        = $opts{'v'} if $opts{'v'};
$debug          = $opts{'d'} if $opts{'d'};

# Check for illegal option combinations
unless ((defined($username) or defined($username_file)) and (defined($host) or defined($host_file))) {
	print $usage;
	exit 1;
}

# Check for strange option combinations
if (
	(defined($host) and defined($host_file))
	or
	(defined($username) and defined($username_file))
) {
	print "WARNING: You specified a lone username or host AND a file of them.  Continuing anyway...\n";
}

# Shovel usernames and host into arrays
if (defined($username_file)) {
	open(FILE, "<$username_file") or die "ERROR: Can't open username file $username_file: $!\n";
	@usernames = map { chomp($_); $_ } <FILE>;
}

if (defined($host_file)) {
	open(FILE, "<$host_file") or die "ERROR: Can't open username file $host_file: $!\n";
	@hosts = map { chomp($_); $_ } <FILE>;
}

if (defined($username)) {
	push @usernames, $username;
}

if (defined($host)) {
	push @hosts, $host;
}

if (defined($host_file) and not @hosts) {
	print "ERROR: Targets file $host_file was empty\n";
	exit 1;
}

if (defined($username_file) and not @usernames) {
	print "ERROR: Username file $username_file was empty\n";
	exit 1;
}

print "Starting finger-user-enum v$VERSION ( http://pentestmonkey.net/tools/finger-user-enum )\n";
print "\n";
print " ----------------------------------------------------------\n";
print "|                   Scan Information                       |\n";
print " ----------------------------------------------------------\n";
print "\n";
print "Worker Processes ......... $max_procs\n";
print "Targets file ............. $host_file\n" if defined($host_file);
print "Usernames file ........... $username_file\n" if defined($username_file);
print "Target count ............. " . scalar(@hosts) . "\n" if @hosts;
print "Username count ........... " . scalar(@usernames) . "\n" if @usernames;
print "Target TCP port .......... $finger_port\n";
print "Query timeout ............ $query_timeout secs\n";
if (defined($relayserver)) {
print "Relay Server ............. $relayserver\n";
} else {
print "Relay Server ............. Not used\n";
}
print "\n";
print "######## Scan started at " . scalar(localtime()) . " #########\n";

# Spawn off correct number of children
foreach my $proc_count (1..$max_procs) {
	socketpair(my $child, my $parent, AF_UNIX, SOCK_STREAM, PF_UNSPEC) or  die "socketpair: $!";
	$child->autoflush(1);
	$parent->autoflush(1);

	# Parent executes this
	if (my $pid = fork) {
		close $parent;
		print "[Parent] Spawned child with PID $pid to do resolving\n" if $debug;
		push @child_handles, $child;

	# Chile executes this
	} else {
		close $child;
		while (1) {
			my $timed_out = 0;

			# Read host and username from parent
			my $line = <$parent>;
			chomp($line);
			my ($host, $username) = $line =~ /^(\S+)\t(.*)$/;

			# Exit if told to by parent
			if ($line eq $kill_child_string) {
				print "[Child $$] Exiting\n" if $debug;
				exit 0;
			}
			
			# Sanity check host and username
			if (defined($host) and defined($username)) {
				print "[Child $$] Passed host $host and username $username\n" if $debug;
			} else {
				print "[Child $$] WARNING: Passed garbage.  Ignoring: $line\n";
				next;
			}

			# Do finger query with timeout
			my $response;
			eval {
				local $SIG{ALRM} = sub { die "alarm\n" };
				alarm $query_timeout;
				my $connect_host;
				if (defined($relayserver)) {
					$connect_host = $relayserver;
				} else {
					$connect_host = $host;
				}
				my $s = IO::Socket::INET->new( 	PeerAddr => $connect_host,
								PeerPort => $finger_port,
								Proto    => 'tcp'
							)
					or die "Can't connect to $host:$finger_port: $!\n";
				if (defined($relayserver)) {
					$s->send($username . "@" . "$host\r\n");
				} else {
					$s->send("$username\r\n");
				}
				$s->recv($response, 10000);
				alarm 0;
			};

			if ($@) {
				$timed_out = 1;
				print "[Child $$] Timeout for username $username on host $host\n" if $debug;
			}

			my $trace;
			if ($debug) {
				$trace = "[Child $$] $username\@$host: ";
			} else {
				$trace = "$username\@$host: ";
			}

			if ($response and not $timed_out) {

				# Negative result against solaris 7
				#
				# blah@10.0.0.1  Login       Name               TTY         Idle    When    Where
				# blah            ???
				if ($response =~ /Login\s+Name\s+TTY\s+Idle\s+When\s+Where.*$username\s+\?\?\?[^<>]+$/s) {
					print $parent $trace . "<no such user>\n";
					next;
				} 
				
				# Negative result for unknow finger daemon
				# It just returns a single "f" - presumably for "false"
				if ($response =~ /\s*f\s*$/) {
					print $parent $trace . "<no such user>\n";
					next;
				}

				#
				# Positive result against solaris 7
				#
				# if ($response =~ /^Login\s+Name\s+TTY\s+Idle\s+When\s+Where.*($username\s+[^?].*)/s) {
				# if ($response =~ /Login\s+Name\s+TTY\s+Idle\s+When\s+Where.*($username.*<.*>.*)/s) {
				if ($response =~ /Login\s+Name\s+TTY\s+Idle\s+When\s+Where.*($username.*)/s) {
					my $username_info = $1;
					$username_info =~ s/[\r\n]/./g; # Reduce to a single line
					print $parent $trace . "$username_info\n";
					next;
				}

				# Assume a positive response if we don't recognise the format
				$response =~ s/[\n\r]/./g;
				print $parent $trace . "$response\n";
				next;
			}

			if ($timed_out) {
				print $parent $trace . "<timeout>\n";
			} else {
				if (!$response) {
					print $parent $trace . "<no result>\n";
				}
			}
		}
		exit;
	}
}

# Fork once more to make a process that will us usernames and hosts
socketpair(my $get_next_query, my $parent, AF_UNIX, SOCK_STREAM, PF_UNSPEC) or  die "socketpair: $!";
$get_next_query->autoflush(1);
$parent->autoflush(1);

# Parent executes this
if (my $pid = fork) {
	close $parent;

# Chile executes this
} else {
	# Generate queries from username-host pairs and send to parent
	foreach my $username (@usernames) {
		foreach my $host (@hosts) {
			my $query = $host . "\t" . $username;
			print "[Query Generator] Sending $query to parent\n" if $debug;
			print $parent "$query\n";
		}
	}

	exit 0;
}

printf "Created %d child processes\n", scalar(@child_handles) if $debug;
my $s = IO::Select->new();
my $s_in = IO::Select->new();
$s->add(@child_handles);
$s_in->add(\*STDIN);
my $timeout = 0; # non-blocking
my $more_queries = 1;
my $outstanding_queries = 0;
my $query_count = 0;
my $result_count = 0;

# Write to each child process once
writeloop: foreach my $write_handle (@child_handles) {
	my $query = <$get_next_query>;
	if ($query) {
		chomp($query);
		print "[Parent] Sending $query to child\n" if $debug;
		print $write_handle "$query\n";
		$outstanding_queries++;
	} else {
		print "[Parent] Quitting main loop.  All queries have been read.\n" if $debug;
		last writeloop;
	}
}

# Keep reading from child processes until there are no more queries left
# Write to a child only after it has been read from
mainloop: while (1) {
	# Wait until there's a child that we can either read from or written to.
	my ($rh_aref) = IO::Select->select($s, undef, undef); # blocking

	print "[Parent] There are " . scalar(@$rh_aref) . " children that can be read from\n" if $debug;

	foreach my $read_handle (@$rh_aref) {
		# Read from child
		chomp(my $line = <$read_handle>);
		if ($verbose == 1 or $debug == 1 or not ($line =~ /<no such user>/ or $line =~ /no result/ or $line =~ /<timeout>/)) {
			print "$line\n";
			$result_count++ unless ($line =~ /<no such user>/ or $line =~ /no result/ or $line =~ /<timeout>/);
		}
		$outstanding_queries--;
		$query_count++;

		# Write to child
		my $query = <$get_next_query>;
		if ($query) {
			chomp($query);
			print "[Parent] Sending $query to child\n" if $debug;
			print $read_handle "$query\n";
			$outstanding_queries++;
		} else {
			print "DEBUG: Quitting main loop.  All queries have been read.\n" if $debug;
			last mainloop;
		}
	}
}

# Wait to get replies back from remaining children
my $count = 0;
readloop: while ($outstanding_queries) {
	my @ready_to_read = $s->can_read(1); # blocking
	foreach my $child_handle (@ready_to_read) {
		print "[Parent] Outstanding queries: $outstanding_queries\n" if $debug;
		chomp(my $line = <$child_handle>);
		if ($verbose == 1 or $debug == 1 or not ($line =~ /<no such user>/ or $line =~ /no result/ or $line =~ /<timeout>/)) {
			print "$line\n";
			$result_count++ unless ($line =~ /<no such user>/ or $line =~ /no result/ or $line =~ /<timeout>/);
		}
		print $child_handle "$kill_child_string\n";
		$s->remove($child_handle);
		$outstanding_queries--;
		$query_count++;
	}
}

# Tell any remaining children to exit
foreach my $handle ($s->handles) {
	print "[Parent] Telling child to exit\n" if $debug;
	print $handle "$kill_child_string\n";
}

# Wait for all children to terminate
while(wait != -1) {};

print "######## Scan completed at " . scalar(localtime()) . " #########\n";
print "$result_count results.\n";
print "\n";
$end_time = time(); # Second granularity only to avoid depending on hires time module
my $run_time = $end_time - $start_time;
$run_time = 1 if $run_time < 1; # Avoid divide by zero
printf "%d queries in %d seconds (%0.1f queries / sec)\n", $query_count, $run_time, $query_count / $run_time;
