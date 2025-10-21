# Installing dependencies

Installing dependencies is handled entirely through **Bun**.\
**Do not** use `npm`, `pnpm`, `yarn`, or any other package manager — they might break some native Bun dependencies.

If you're not already inside the repository, move into it:

`cd node`

Then install the dependencies:

`bun install`

Sometimes Bun doesn't automatically trust postinstall scripts for new repositories.

The warning might look like this:

`Blocked 8 postinstalls. Run bun pm untrusted for details.`\
\
If you see a warning about trust, run:

`bun pm trust --all`

This will allow Bun to build the necessary native modules.
