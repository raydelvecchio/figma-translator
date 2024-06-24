# Figma to UI Translator
Given any Figma file, convert it into a real, actionable React environment in code. ***Your high school level Frontend Software engineer!***

# Details
* Input a Figma file ID, found on the web in `https://figma.com/design/<YOUR_ID_HERE>`
* A `yarn` react environment will spin up with your component created and running!
* Writes all images and code samples to their own folders for your viewing
* The translator has access to Javascript, React, Bootstrap, Tailwind, and React Icons to complete the code
* You can toggle the creation of a test environment and only output the code files if you'd like as well!

# Example
```python
from figmatranslator import FigmaTranslator
ft = FigmaTranslator(project_name="my_first_project", test_environment=True)
ft.translate(figma_file_id="<YOUR ID HERE>", output_image_filename="example.png")
```
* In this code sample, the following will occur:
    * A new test environment called my_first_project will be created
    * Images of your Figma file will be downloaded
    * Your Figma file will be converted to code, saved to a file, then integrated into the test environment
    * The test environment will start!

# Limitations
* Currently, we can only pull one screen from your Figma file
* Any external imports, notably Shadcn, are not supported


# Examples

Here are some examples of how the Figma to UI Translator works:

## Input Figma Design
![Figma Waitlist Design](examples/figma_waitlist.png)

This image shows an example Figma design for a waitlist signup page.

## Generated React UI
![Generated React UI](examples/generated_waitlist.png)

This image demonstrates the React UI component generated from the Figma design above. As you can see, the translator accurately converts the visual design into functional React code, including layout, styling, and interactive elements. ***It did this one-shot, with no extra prompting or agentic loops required***.
