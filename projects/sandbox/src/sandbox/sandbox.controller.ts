import { Controller, Post, Body, HttpCode, Get } from '@nestjs/common';
import { RunCodeDto } from './dto/create-sandbox.dto';
import { runJsSandbox, runPythonSandbox } from './utils';

@Controller('sandbox')
export class SandboxController {
  constructor() {}

  @Get()
  getInfo() {
    return {
      message: 'FastGPT Sandbox Service',
      version: '1.0.0',
      endpoints: {
        'POST /sandbox/js': 'Execute JavaScript code',
        'POST /sandbox/python': 'Execute Python code',
        'GET /api': 'Swagger API documentation'
      }
    };
  }

  @Post('/js')
  @HttpCode(200)
  runJs(@Body() codeProps: RunCodeDto) {
    return runJsSandbox(codeProps);
  }

  @Post('/python')
  @HttpCode(200)
  runPython(@Body() codeProps: RunCodeDto) {
    return runPythonSandbox(codeProps);
  }
}
