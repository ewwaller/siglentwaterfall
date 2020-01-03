<body>
  <div class="section" id="siglentwaterfall">
<h1>SiglentWaterfall<a class="headerlink" href="#siglentwaterfall" title="Permalink to this headline">¶</a></h1>
<div class="section" id="introduction">
<h2>Introduction<a class="headerlink" href="#introduction" title="Permalink to this headline">¶</a></h2>
<p>This program obtains trace information from a Siglent oscilloscope and
displays them as a three dimension plot displaying a scrolling history
of recent traces.  The plot can be rotated and zoomed in our out
using point devices.</p>
<p>The application is written in <em>Python3</em> on and uses multi-programming
techniques to allow the program to use multiple cores.</p>
<p>Communication with the oscilloscope uses the <em>visa</em> instrument control
infrastructure.</p>
</div>
<div class="section" id="usage">
<h2>Usage<a class="headerlink" href="#usage" title="Permalink to this headline">¶</a></h2>
<p>To start the program from the command line, see the following usage.:</p>
<div class="highlight-text notranslate"><div class="highlight"><pre><span></span>Usage: siglent [OPTIONS]

  Siglent

  Display a YT display and (optionally) a waterfall display of scope traces
  obtained from an SDS 1204X-E oscilloscope.

Options:
  -r, --rows INTEGER       Rows in waterfall display (number of traces)
  -c, --cols INTEGER       columns in waterfall display (samples/trace)
  --waterfall              Show the 3D Display
  --channel TEXT           Scope channel to capture (default=C1)
  -n, --name TEXT          VISA Address of the oscilloscope  [required]
  -v, --verbose            Be verbose.  Invoke twice for more verbosity
  -L, --log-file PATH      Log file Name.
  -t, --timeout INTEGER    Foreground process timeout in seconds (debug only)
  -b, --bgtimeout INTEGER  Background process timeout in seconds (debug only)
  --help                   Show this message and exit.
</pre></div>
</div>
<p>For example:</p>
<div class="highlight-none notranslate"><div class="highlight"><pre><span></span>siglent -n tcpip::192.168.1.201 -vv --waterfall
</pre></div>
</div>
<p>Will start the <em>Siglent Waterfall</em> program reading from the
instrument at IP Address 192,168.1.201, being extremely verbose (debug
level), and will display both the 2D and 3D displays.</p>
<div class="highlight-none notranslate"><div class="highlight"><pre><span></span>siglent -n tcpip::192.168.1.201 -v
</pre></div>
</div>
<p>Will start the <em>Siglent Waterfall</em> program reading from the
instrument at IP Address 192,168.1.201, being a little verbose (info
level), and will display only 2D and 3D display.</p>
</div>
</div>
<div class="section" id="siglentwaterfall-modules">
<h1>SiglentWaterfall  Modules<a class="headerlink" href="#siglentwaterfall-modules" title="Permalink to this headline">¶</a></h1>
<div class="section" id="module-__main__">
<span id="main"></span><h2>Main<a class="headerlink" href="#module-__main__" title="Permalink to this headline">¶</a></h2>
</div>
<div class="section" id="module-background">
<span id="background"></span><h2>Background<a class="headerlink" href="#module-background" title="Permalink to this headline">¶</a></h2>
<p>Generate a stream of vectors read from a siglent oscilloscope</p>
<dl class="class">
<dt id="background.Acquire">
<em class="property">class </em><code class="sig-prename descclassname">background.</code><code class="sig-name descname">Acquire</code><span class="sig-paren">(</span><em class="sig-param">address</em>, <em class="sig-param">channel</em>, <em class="sig-param">cols</em><span class="sig-paren">)</span><a class="headerlink" href="#background.Acquire" title="Permalink to this definition">¶</a></dt>
<dd><p>Acquire traces from the oscilloscope</p>
<p>This class sets up the oscilloscope, then reads data from it
continuously, posting those trace information to a queue that is
processed by the main program.  This code is run in a multiprocess
environment allowing it to run independently of the main program.
Hopefully, it runs on its own core.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>address</strong> (<em>str</em>) – The <em>visa</em> address of the instrument</p></li>
<li><p><strong>channel</strong> (<em>str</em>) – The channel to read from the scope.  Defaults
to ‘C1’.  Values can be <em>C1, C2, C3, C4</em> or <em>math</em></p></li>
<li><p><strong>cols</strong> (<em>int</em>) – The number of points to place in each vector.
This controls the <em>skip factor</em> in the waveform
setup. This decimates the 14K (or more) points in
the scope memory down to a manaeable number of
points</p></li>
</ul>
</dd>
</dl>
<dl class="method">
<dt id="background.Acquire.update">
<code class="sig-name descname">update</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#background.Acquire.update" title="Permalink to this definition">¶</a></dt>
<dd><p>Read the next trace from the oscillocope</p>
<p>Read parameters as to the format and scale of the trace, read
the raw data points, apply scale and offset information to
the data</p>
<dl class="simple">
<dt>Returns: <em>False</em> if there is an error.  Otherwise, return a</dt><dd><p>tuple of two equal size lists of float.  The first
element is a list of <em>float</em> representing time
values, and a list of <em>float</em> representing voltages.</p>
</dd>
</dl>
</dd></dl>

</dd></dl>

<dl class="exception">
<dt id="background.ScopeInitializationError">
<em class="property">exception </em><code class="sig-prename descclassname">background.</code><code class="sig-name descname">ScopeInitializationError</code><a class="headerlink" href="#background.ScopeInitializationError" title="Permalink to this definition">¶</a></dt>
<dd></dd></dl>

<dl class="function">
<dt id="background.main">
<code class="sig-prename descclassname">background.</code><code class="sig-name descname">main</code><span class="sig-paren">(</span><em class="sig-param">cols</em>, <em class="sig-param">timeout</em>, <em class="sig-param">address</em>, <em class="sig-param">channel</em>, <em class="sig-param">pipe</em><span class="sig-paren">)</span><a class="headerlink" href="#background.main" title="Permalink to this definition">¶</a></dt>
<dd><p>Stream traces from a Siglent oscilloscope to a pipe.</p>
<p>Read traces from a Siglent 1204x-E oscilloscope and stream those
traces to the main program through a pipe.  We also will receive
commands through that pipe.  Handle those commands and respnd to
those cmmands through the pipe as well.  Commands and responses to
those commands will be of the type ‘Message’ from the class
defined above.  The traces are sent as a 2-tuple of lists.  The
first list represents the time values of the samples, while the
second list represents the voltages at the time values.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>cols</strong> (<em>int</em>) – The expected size of the lists to be sent through
the pipe.</p></li>
<li><p><strong>timeout</strong> (<em>int</em>) – The maximum time this process is to run.  0
implys no timeout</p></li>
<li><p><strong>address</strong> (<em>str</em>) – The <em>visa</em> address of the oscilloscope</p></li>
<li><p><strong>channel</strong> (<em>str</em>) – The name of the oscilloscope channel to stream.</p></li>
<li><p><strong>pipe</strong> (<em>pipe</em>) – The pipe through which data are communicated to
and from the main program.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p><em>None</em></p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p>None</p>
</dd>
</dl>
</dd></dl>

</div>
<div class="section" id="module-log">
<span id="log"></span><h2>Log<a class="headerlink" href="#module-log" title="Permalink to this headline">¶</a></h2>
<dl class="function">
<dt id="log.setLog">
<code class="sig-prename descclassname">log.</code><code class="sig-name descname">setLog</code><span class="sig-paren">(</span><em class="sig-param">LogLevelStr</em><span class="sig-paren">)</span><a class="headerlink" href="#log.setLog" title="Permalink to this definition">¶</a></dt>
<dd><p>Set the log level to be used during this run.
This program uses logging to provide warning, info, and debug
level messages. Wwarnings are always enabled.  info level messages
are considered to be “Verbose”.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>LogLevelStr</strong> – A string representing on of the members of logging that
define log levels (“CRITICAL”, DEBUG”, “ERROR”, “FATAL”
(“INFO”, “NOTSET”, WARN, “WARNING”)</p>
</dd>
</dl>
</dd></dl>

</div>
<div class="section" id="module-TwoDGraph">
<span id="twodgraph"></span><h2>TwoDGraph<a class="headerlink" href="#module-TwoDGraph" title="Permalink to this headline">¶</a></h2>
<dl class="class">
<dt id="TwoDGraph.Graph">
<em class="property">class </em><code class="sig-prename descclassname">TwoDGraph.</code><code class="sig-name descname">Graph</code><span class="sig-paren">(</span><em class="sig-param">rows</em>, <em class="sig-param">title='YT Display'</em><span class="sig-paren">)</span><a class="headerlink" href="#TwoDGraph.Graph" title="Permalink to this definition">¶</a></dt>
<dd><p>Create a window in which to display the YT display</p>
<p>The window contains two grids and the YT display.  The axes are
time, and amplitude.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>rows</strong> (<em>int</em>) – Defines the horizontal size of plot in samples.</p>
</dd>
<dt class="field-even">Keyword Arguments</dt>
<dd class="field-even"><p><strong>title</strong> (<em>str</em>) – The name of the window. Defaults to <em>YT Display</em></p>
</dd>
</dl>
<dl class="attribute">
<dt id="TwoDGraph.Graph.np">
<code class="sig-name descname">np</code><em class="property"> = &lt;module 'numpy' from '/usr/lib/python3.8/site-packages/numpy/__init__.py'&gt;</em><a class="headerlink" href="#TwoDGraph.Graph.np" title="Permalink to this definition">¶</a></dt>
<dd></dd></dl>

<dl class="attribute">
<dt id="TwoDGraph.Graph.pg">
<code class="sig-name descname">pg</code><em class="property"> = &lt;module 'pyqtgraph' from '/usr/lib/python3.8/site-packages/pyqtgraph/__init__.py'&gt;</em><a class="headerlink" href="#TwoDGraph.Graph.pg" title="Permalink to this definition">¶</a></dt>
<dd></dd></dl>

<dl class="method">
<dt id="TwoDGraph.Graph.update">
<code class="sig-name descname">update</code><span class="sig-paren">(</span><em class="sig-param">data</em><span class="sig-paren">)</span><a class="headerlink" href="#TwoDGraph.Graph.update" title="Permalink to this definition">¶</a></dt>
<dd><p>Obtain next chunk of data, update the waterfall display</p>
</dd></dl>

</dd></dl>

</div>
<div class="section" id="module-ThreeDGraph">
<span id="threedgraph"></span><h2>ThreeDGraph<a class="headerlink" href="#module-ThreeDGraph" title="Permalink to this headline">¶</a></h2>
<dl class="class">
<dt id="ThreeDGraph.Graph">
<em class="property">class </em><code class="sig-prename descclassname">ThreeDGraph.</code><code class="sig-name descname">Graph</code><span class="sig-paren">(</span><em class="sig-param">rows</em>, <em class="sig-param">cols</em>, <em class="sig-param">title='3D Waterfall Display'</em>, <em class="sig-param">distance=50</em><span class="sig-paren">)</span><a class="headerlink" href="#ThreeDGraph.Graph" title="Permalink to this definition">¶</a></dt>
<dd><p>Create a window in which to display the 3d display</p>
<p>The window contains two grids and the 3d display.  The axes are
time (history of former traces) , time (for a given trace) and
amplitude of the points in the trace.  The grids are on the
(history)time-amplitude and (history) time-time axes.  No grid is
generated for the (trace) time-amplitude axes so as not to occlude
the line-of-site of the display</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>rows</strong> (<em>int</em>) – Defines the size of the waterfall in rows.  This
value represents the numper of points per trace.</p></li>
<li><p><strong>cols</strong> (<em>int</em>) – Defines the size of the waterfall in columns.  This
value represents the depth of the storage.  This
is the number of traces to display</p></li>
</ul>
</dd>
<dt class="field-even">Keyword Arguments</dt>
<dd class="field-even"><ul class="simple">
<li><p><strong>title</strong> (<em>str</em>) – The name of the waterfall window.  Defaults to
<em>3d Waterfall Display</em></p></li>
<li><p><strong>distance</strong> (<em>int</em>) – The inital distance of the observer from the
3D display</p></li>
</ul>
</dd>
</dl>
<dl class="attribute">
<dt id="ThreeDGraph.Graph.np">
<code class="sig-name descname">np</code><em class="property"> = &lt;module 'numpy' from '/usr/lib/python3.8/site-packages/numpy/__init__.py'&gt;</em><a class="headerlink" href="#ThreeDGraph.Graph.np" title="Permalink to this definition">¶</a></dt>
<dd></dd></dl>

<dl class="attribute">
<dt id="ThreeDGraph.Graph.pg">
<code class="sig-name descname">pg</code><em class="property"> = &lt;module 'pyqtgraph' from '/usr/lib/python3.8/site-packages/pyqtgraph/__init__.py'&gt;</em><a class="headerlink" href="#ThreeDGraph.Graph.pg" title="Permalink to this definition">¶</a></dt>
<dd></dd></dl>

<dl class="method">
<dt id="ThreeDGraph.Graph.update">
<code class="sig-name descname">update</code><span class="sig-paren">(</span><em class="sig-param">data</em><span class="sig-paren">)</span><a class="headerlink" href="#ThreeDGraph.Graph.update" title="Permalink to this definition">¶</a></dt>
<dd><p>Obtain next chunk of data, update the waterfall display</p>
</dd></dl>

</dd></dl>

</div>
</div>
<div class="section" id="license">
<h1>License<a class="headerlink" href="#license" title="Permalink to this headline">¶</a></h1>
<p>This program is licensed under the MIT license.</p>
<p>Copyright (c) 2020 Eric Waller</p>
<p>Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:</p>
<p>The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.</p>
<p>THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.</p>
</div>
<div class="section" id="third-party-software">
<h1>Third Party Software<a class="headerlink" href="#third-party-software" title="Permalink to this headline">¶</a></h1>
<p>The following modules, not provided by Python or the <em>Siglent Waterfall</em>
repository, are required at run time and are installed automatically
by <em>pip</em>:</p>
<table class="docutils align-default">
<colgroup>
<col style="width: 34%" />
<col style="width: 21%" />
<col style="width: 45%" />
</colgroup>
<tbody>
<tr class="row-odd"><td><p>Module Name</p></td>
<td><p>Version</p></td>
<td><p>Description</p></td>
</tr>
<tr class="row-even"><td><p>Python</p></td>
<td><p>3.8</p></td>
<td><p>Interpreter</p></td>
</tr>
<tr class="row-odd"><td><p>Click</p></td>
<td><p>7.0</p></td>
<td><p>Command line interface</p></td>
</tr>
<tr class="row-even"><td><p>numpy</p></td>
<td><p>17.4</p></td>
<td><p>Vector Math</p></td>
</tr>
<tr class="row-odd"><td><p>PyOpenGL</p></td>
<td><p>3.1.0</p></td>
<td><p>3D graphics engine</p></td>
</tr>
<tr class="row-even"><td><p>PyQt5</p></td>
<td><p>5.13.2</p></td>
<td><p>GUI subsystem</p></td>
</tr>
<tr class="row-odd"><td><p>PyQt5-sip</p></td>
<td><p>12.7.0</p></td>
<td><p>GUI subsystem</p></td>
</tr>
<tr class="row-even"><td><p>pyqtgraph</p></td>
<td><p>0.10.0</p></td>
<td><p>graphing package</p></td>
</tr>
<tr class="row-odd"><td><p>pyVISA</p></td>
<td><p>1.10.1</p></td>
<td><p>Instrument control</p></td>
</tr>
<tr class="row-even"><td><p>scipy</p></td>
<td><p>1.3.3</p></td>
<td><p>Vector math</p></td>
</tr>
</tbody>
</table>
<p>This program does use <em>Sphinx</em> to automatically generate
documentation from the <em>doc</em> strings in the Python code itself.
Sphinx can create man files, HTML files, pdf files, and others.  This
program uses the HTML documentation for the web application and pdf
files for written manuals.  It also generates man files for reference
when running on Linux from a command line.</p>
<p>The following top level modules are required to build the documentation for this
program suite.  These modules may have dependencies of their own and
are system dependent.  These are not automatically installed.</p>
<table class="docutils align-default">
<colgroup>
<col style="width: 22%" />
<col style="width: 14%" />
<col style="width: 35%" />
<col style="width: 29%" />
</colgroup>
<tbody>
<tr class="row-odd"><td><p>Module Name</p></td>
<td><p>Version</p></td>
<td><p>Organization</p></td>
<td><p>Description</p></td>
</tr>
<tr class="row-even"><td><p>Sphinx</p></td>
<td><p>1.8.1</p></td>
<td><p><a class="reference external" href="http://www.sphinx-doc.org/">http://www.sphinx-doc.org/</a></p></td>
<td><p>Documentation Generator</p></td>
</tr>
<tr class="row-odd"><td><p>texlive</p></td>
<td><p>2018.48568</p></td>
<td><p><a class="reference external" href="http://tug.org/">http://tug.org/</a></p></td>
<td><p>Web Template Engine</p></td>
</tr>
</tbody>
</table>
<p>To build the HTML documentation, from the root directory, run:</p>
<blockquote>
<div><p><em>make html</em></p>
</div></blockquote>
<p>To build the pdf documentation, from the root directory, run:</p>
<blockquote>
<div><p><em>make latexpdf</em></p>
</div></blockquote>
<p>To build the <em>man</em> documentation, from the root directory, run:</p>
<blockquote>
<div><p><em>make man</em></p>
</div></blockquote>
</div>
<div class="section" id="indices-and-tables">

  </body>
</html>
