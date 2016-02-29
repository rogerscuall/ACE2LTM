<p>Synopsis</p>
<p>Project to help in the migration from Cisco ACE to F5 LTM, all nodes, pools and virtual servers can be migrated to tmsh syntax. Also some counts of the number of objects can be done.</p>
<p>Code Example</p>
<p> ``` convert.py ace_config.txt ```

Will create file in the same directory with the configuration of the LTM ready to paste in the tmsh cli.
```convert.py ace_config.txt -c"
Provide the number of nodes, pools and virtual servers in the ACE configuration.
</p>
<p>Motivation</p>
<p></p>
<p>Installation</p>
<p>Provide code examples and explanations of how to get the project.</p>
<p>API Reference</p>
<p>Depending on the size of the project, if it is small and simple enough the reference docs can be added to the README. For medium size to larger projects it is important to at least provide a link to where the API reference docs live.</p>
<p>Tests</p>
<p>Describe and show how to run the tests with code examples.</p>
<p>Contributors</p>
<p>Let people know how they can dive into the project, include important links to things like issue trackers, irc, twitter accounts if applicable.</p>
<p>License</p>
<p>A short snippet describing the license (MIT, Apache, etc.)</p>