# Siri for Network Configuration
### Abstract
Configuring networks is pivotal for the functioning, dependability, and security of expansive cloud systems. While tools like Batfish exist for identifying network configuration errors, they lack the capability to rectify them. Consequently, rectifying these errors remains predominantly a manual and intricate process, prone to mistakes. Addressing the challenge of efficiently validating and correcting network configurations with minimal engineering intervention is an ongoing research endeavor. The recent progress in code generation by Large Language Models (LLMs) and the widespread adoption of the "configuration-as-code" paradigm offer new insights into tackling this issue.

This study explores the potential of a cutting-edge LLM, GPT-4 Turbo, in identifying and rectifying network configuration errors. The evaluation involves 100 flawed network configuration files, encompassing five commonly encountered fault categories in a real-world setting. The findings indicate that GPT-4 Turbo successfully identifies and rectifies 70% of these faults without contextual information, improving to 85% accuracy through in-context learning.

Additionally, the project outlines avenues for future research, highlighting notable side-effects such as hallucinations observed in LLM-aided configuration validation and correction, as evidenced by specific case studies.

### Summary
We conducted a study on the effectiveness of GPT-4 Turbo (LLM) in identifying and correcting network configuration faults. We used Batfish as a post-correction configuration checker. Our results showed that GPT-4 Turbo performed well in detecting syntax-related faults but struggled with functional faults that required specific domain-driven contexts.

We also discussed the limitations of existing validation tools, such as Batfish, which heavily rely on human expert-designed test cases and lack detailed error reporting capabilities. We highlighted the challenges in integrating LLMs with validation tools, including the mismatched input/output formats and the lack of mechanisms to provide domain-specific context to LLMs.

To address these limitations, we proposed enhancing the error reporting capabilities of validation tools to align with LLM requirements and improving the provision of domain-specific context to LLMs. We believe that combining LLMs and validation tools can lead to a more effective and user-friendly configuration validation process.

Overall, our study provides insights into the capabilities and limitations of LLMs in network configuration validation and highlights potential research directions for LLM-aided configuration validation with validation tools in the loop.


### Usage
- Default configuration: `as2border2.cfg`
- Fault injector: `batfish_injector.py`
- Fault injected configurations by fault category: `/injected_files`
- LLM prompt: `prompt.md` and `prompt_context.md`
- LLM output for each fault injected configuration: `/output`