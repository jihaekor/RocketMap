# RocketMap tutorial completion for accounts (up to Level 2)

This is documentation to complete the Pokemon GO Tutorial for a number of
accounts while simultaneously become level 2 when completing it next to a
Pokestop due to the "First Pokestop of the Day" bonus.

## Instruction
* We assume you are running a basic RocketMap installation. It is best to run
the tutorial with hashing service on newest API to not get your fresh accounts
becoming flagged.
* Set up an instance with a config file and make some changes to it which let
the tutorial run smooth and fast enough to go through a batch of accounts.
* Config changes are:
	* Location next to at least one known Pokestop, a cluster ist better.
	* Set step distance to ``st: 1``.
	* Set scan delay ``sd`` to a value which provides enough calls during the
	following set search time (a good value is around ``sd: 15`` or lower).
	* Set the account search interval to around ``asi: 120``.
	* Set the account rest interval as high as possible that all accounts get
	cycled and none returns, a safe value is ``ari: 36000``.
	* Set login delay at least to ``login_delay: 1`` to avoid throttling.
* Put your accounts into a ``accounts.csv`` file and refer to it in your
process with ``-ac PATH/accounts.csv`` or in the config file with
``accountcsv: PATH/accounts.csv``.
* Set your simultaneously working accounts, with ``-w`` as process flag, to a
reasonable number, considering hash key limit and throttling. You can at least
have 10 accounts running at the same time.
* If you are not using fresh accounts and you are not running hash service,
prepare for occuring captchas. Set up your RocketMap accordingly.
* Enable ``-v`` in process if you want to see it working in log.
* Let it run and your accounts will complete the tutorial and rise to Level 2.
