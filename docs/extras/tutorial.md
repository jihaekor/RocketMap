# RocketMap tutorial completion for accounts (up to Level 2)

This is documentation to complete the Pokemon GO Tutorial for a number of accounts while simultaneously become level 2 when completing it next to a Pokestop due to the "First Pokestop of the Day" bonus.

## Instruction
* We assume you are running a basic RocketMap installation. It is best to run the tutorial with hashing service on newest API to not get your fresh accounts becoming flagged
* Set up an instance with a config file and make some changes to it which let the tutorial run smooth and fast enough to go through a batch of accounts.
* Config changes are:
	* location next to at least one known Pokestop, a cluster ist better.
	* set step distance to ``st: 1``
	* set scan delay ``sd`` to a value which provides enough calls during the following set search time (a good value is around ``sd: 15`` or lower)
	* set the account search interval to around ``-asi: 120``
	* set the account rest interval as high as possible that all accounts get cycled and none returns, a safe value is ``-ari: 36000``
* put your accounts for the tutorial and level up into a ``accounts.csv`` file and refer to it in your process with ``-ac PATH/accounts.csv`` or in the config file with ``accountcsv: PATH/accounts.csv``.
* if you are not using fresh accounts and you are not running has service, prepare for occuring captchas. Set up your RocketMap accordingly.
* Let it run and watch it complete the tutorials as well as getting your accounts up to Level 2



