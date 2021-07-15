# SENTINEL NETWORK

A Business to Business authentication service, which is database leak tolerant.


## v1.0 Centralized Auth 

We use an exclusive key which is read-only by the administrator, and use this key to generate a random hash for a given email and password. This is done on a sub-net within the network. 

The sub-net is callable by administrator run scripts (figure out a little). This sub-net is called while generating a mapping number for authentication. The random mapper is as secure as the exclusive (additive) security of admin's system plus, admin's key is.

This key is used as a mapper to find the E-mail ID associated, let it be `E1`.
Now, we find HASH using hash of password `H1`, and `E1` along with mapper number `n`.
We also apply salting to H1 to make it `H2` = salt1+`H1`+salt2
> I am trying to make the salt, a function of the input hash itself.
The expected matching hash should be H(H(`E1`+`n`)+H(`n`+`H2`))


Note that to make the password database like a normal salted password database, we would require to know the number n, which implies knowing the admin's key. This in turn implies having admin access to the sub-net.

Notice that this means a rudimentary database leak cannot imply a password leak and in light terms, security of any password is : 

Security(password) >= (system_security(ADMIN_SYSTEM)+system_security(ADMIN_KEY))*(crypto_security(password))

### Drawbacks 

1. Increased latency
2. Data leak is also a potential system_security flaw, so if an infiltrator can break-into database, he/she can break into the system itself too.

Do-over (v1.1)
We can use concept of  [Obfuscated Scripts](https://unix.stackexchange.com/questions/90178/how-can-i-either-encrypt-or-render-my-shell-script-unreadable/178325).

But this again has [problems](https://www.linuxjournal.com/article/8256)

## Decentralized Authentication